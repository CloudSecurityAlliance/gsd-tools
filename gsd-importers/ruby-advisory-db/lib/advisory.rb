require 'yaml'
require 'json'
require 'date'
require 'active_support'
require 'active_support/core_ext'

module GSD
  module RubySecImporter
    class Advisory
      def initialize(yaml_content: nil, yaml_file: nil)
        if yaml_content.present? && yaml_file.present?
          raise ArgumentError,
            'Provided both yaml content and a yaml file, use one or the other!'
        end

        if yaml_file.present?
          load_from_file(yaml_file)
        elsif yaml_content.present?
          load_from_content(yaml_content)
        end
      end

      def gsd_id
        @cve.present? ? "GSD-#{@cve}" : nil
      end

      def gsd_file_path
        return nil if invalid?

        identifier = gsd_id
        year = identifier.split('-')[1]
        thousands = identifier.split('-')[2][0..-4] + 'xxx'

        "#{year}/#{thousands}/#{identifier}.json"
      end

      def valid?
        required_fields_present? && @cve.present?
      end

      def invalid?
        !valid?
      end

      def to_h
        {
          gem: @gem,
          library: @library,
          framework: @framework,
          platform: @platform,
          cve: @cve,
          osvdb: @osvdb,
          ghsa: @ghsa,
          url: @url,
          title: @title,
          date: @date,
          description: @description,
          cvss_v2: @cvss_v2,
          cvss_v3: @cvss_v3,
          unaffected_versions: @unaffected_versions,
          patched_versions: @patched_versions,
          related: @related,
          notes: @notes
        }
      end

      def to_osv
        if invalid?
          raise ArgumentError,
            'Invalid Advisory! Check YAML against schema'
        end

        osv = {}

        published_date = @date.is_a?(Date) ? @date : Date.parse(@date)
        published_timestamp = published_date.to_time.utc.
          strftime('%Y-%m-%dT%H:%M:%S.%L%Z').gsub('UTC', 'Z')

        cve_id = @cve.present? ? "CVE-#{@cve}" : nil
        osvdb_id = @osvdb.present? ? "OSVDB-#{@osvdb}" : nil
        ghsa_id = @ghsa.present? ? "GHSA-#{@ghsa}" : nil
        related_cve_ids = @related.present? ? (@related['cve'] || []).map { |cve| "CVE-#{cve}" } : nil
        related_ghsa_ids = @related.present? ? (@related['ghsa'] || []).map { |ghsa| "GHSA-#{ghsa}" } : nil
        related_osvdb_ids = @related.present? ? (@related['osvdb'] || []).map { |osvdb| "OSVDB-#{osvdb}" } : nil
        related_urls =
          if @related.present?
            (@related['url'] || []).map do |url|
              {
                'type': 'WEB',
                'url': url
              }
            end
          else
            nil
          end
        cvss_v2 = @cvss_v2.present? ? { 'type': 'CVSS_V2', 'score': @cvss_v2 } : nil
        cvss_v3 = @cvss_v3.present? ? { 'type': 'CVSS_V3', 'score': @cvss_v3 } : nil
        # Extracting the versions into a format compatible with OSV is proving challenging...
        affected_ranges = nil

        osv['schema_version'] = '1.4.0'
        osv['id'] = gsd_id
        osv['modified'] = published_timestamp
        osv['published'] = published_timestamp
        osv['withdrawn'] = nil
        osv['aliases'] = [cve_id, osvdb_id, ghsa_id].compact.uniq
        osv['related'] = [
          related_cve_ids, related_ghsa_ids, related_osvdb_ids
        ].flatten.compact.uniq if @related.present?
        osv['summary'] = @title
        osv['details'] = @description
        osv['severity'] = [cvss_v2, cvss_v3].compact
        osv['affected'] = [
          {
            'package': {
              'ecosystem': 'RubyGems',
              'name': @gem,
              'purl': "pkg:gem/#{@gem}"
            }
            # TODO: Add ranges
          }
        ]
        osv['references'] = [
          {
            'type': 'WEB',
            'url': @url
          },
          related_urls
        ].flatten.compact.uniq
        osv['credits'] = []
        osv['database_specific'] = nil

        # Clear out empty arrays
        osv.each do |key, value|
          osv[key] = nil if value.is_a?(Array) && value.empty?
        end

        osv.compact
      end

      private

      # Per: https://github.com/rubysec/ruby-advisory-db#schema
      def required_fields_present?
        @gem.present? &&
        @url.present? &&
        @title.present? &&
        @date.present? &&
        @description.present?
      end

      def load_from_file(yaml_file)
        yaml_content = YAML.load_file(yaml_file, permitted_classes: [Date])
        load_from_content(yaml_content)
      end

      def load_from_content(yaml_content)
        yaml_content = YAML.load(yaml_content) if yaml_content.is_a?(String)
        unless yaml_content.present? && yaml_content.is_a?(Hash)
          raise ArgumentError, "Must pass a yaml string or hash"
        end

        @gem = yaml_content['gem']
        @library = yaml_content['library']
        @framework = yaml_content['framework']
        @platform = yaml_content['platform']
        @cve = yaml_content['cve']
        @osvdb = yaml_content['osvdb']
        @ghsa = yaml_content['ghsa']
        @url = yaml_content['url']
        @title = yaml_content['title']
        @date = yaml_content['date']
        @description = yaml_content['description']
        @cvss_v2 = yaml_content['cvss_v2']
        @cvss_v3 = yaml_content['cvss_v3']
        @unaffected_versions = yaml_content['unaffected_versions']
        @patched_versions = yaml_content['patched_versions']
        @related = yaml_content['related']
        @notes = yaml_content['notes']
      end
    end
  end
end
