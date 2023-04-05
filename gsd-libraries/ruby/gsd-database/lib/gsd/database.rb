require 'git'
require 'json'

module GSD
  class Database
    attr_reader :work_branch, :git_repo, :git_fork, :repo_path, :git, :default_branch

    def initialize(work_branch:, git_repo:, git_fork:, repo_path:)
      @work_branch = work_branch
      @git_repo = git_repo
      @git_fork = git_fork
      @repo_path = repo_path
      # To be set by calling sync
      @git = nil
      @default_branch = nil
    end

    def sync!
      if exists?
        open_repo
      else
        clone_repo
      end

      @default_branch = Git.default_branch(@git_repo)

      prepare_work_branch
    end

    # Find an ID by alias
    def find_by_alias(alias)
      nil
    end

    # TODO: Update to take in GSD ID rather than path
    def modify(file_path, &block)
      raw_json_data = File.read(file_path)
      old_gsd_entry = JSON.parse(raw_json_data)
      new_gsd_entry = old_gsd_entry.deep_dup

      yield new_gsd_entry

      if new_gsd_entry != old_gsd_entry
        indent = json_indent_value(
          parsed_json: old_gsd_entry,
          raw_json: raw_json_data,
          gsd_id: new_gsd_entry['gsd']['osvSchema']['id']
        )
        # Sort by key and include a trailing newline
        contents = json_string(input: new_gsd_entry.sort.to_h, indent: indent) + "\n"
        File.write(file_path, contents)
        add_file(file_path)
        puts "Staged changes!"
      else
        puts "No changes!"
      end
    end

    def save!
      status = @git.status
      staged_files = status.changed.merge(status.added)
      commit("Sync Ruby Advisory DB\n\n#{staged_files.count} IDs have been updated.")
    end

    def push!
      @git.push('fork', @work_branch, force: true)
    end

    def add_file(file_path)
      @git.add(file_path)
    end

    def commit(message)
      @git.commit(message)
    end

    private

    def json_string(input:, indent:, ascii_only: false)
      JSON.pretty_generate(input, indent: indent, ascii_only: ascii_only).gsub(/\[\s*\]/, '[]')
    end

    def exists?
      File.directory?(@repo_path) &&
      !(Dir.entries(@repo_path) - %w[. ..]).empty?
    end

    def open_repo
      @git = Git.open(@repo_path)
      fetch_remotes
    end

    def clone_repo
      @git = Git.clone(@git_repo, @repo_path)
      @git.add_remote('fork', @git_fork)
      fetch_remotes
    end

    def fetch_remotes
      @git.fetch('origin')
      @git.fetch('fork')
    end

    def prepare_work_branch
      @git.branch(@work_branch).checkout
      latest_commit = @git.remote('origin').branch(@default_branch).gcommit
      @git.reset_hard(latest_commit)
    end

    def json_indent_value(parsed_json:, raw_json:, gsd_id:)
      two_spaces = json_string(input: parsed_json, indent: '  ')
      four_spaces = json_string(input: parsed_json, indent: '    ')
      two_spaces_with_newline = two_spaces + "\n"
      four_spaces_with_newline = four_spaces + "\n"
      two_spaces_ascii_only = json_string(input: parsed_json, indent: '  ', ascii_only: true)
      four_spaces_ascii_only = json_string(input: parsed_json, indent: '    ', ascii_only: true)
      variations_of_two_spaces = [two_spaces, two_spaces_with_newline, two_spaces_ascii_only]
      variations_of_four_spaces = [four_spaces, four_spaces_with_newline, four_spaces_ascii_only]
      if variations_of_two_spaces.include?(raw_json)
        '  '
      elsif variations_of_four_spaces.include?(raw_json)
        '    '
      else
        puts 'Failed to auto-detect spacing, falling back to ID range assumptions'
        # GSD is 2021 or newer, and 1000000+, assume 2 spaces
        if gsd_id.match?(/^GSD-202[1-9]-\d{7,}$/)
          puts 'Newer ID in the million plus range, assuming 2 spaces'
          '  '
        # Valid ID, but older than 2021 or sub-million range, assume 4 spaces
        elsif gsd_id.match?(/^GSD-\d{4}-\d{4,}$/)
          puts 'Older ID or sub-million range, assuming 4 spaces'
          '    '
        else
          puts 'Invalid ID! All bets are off, defaulting to 2 spaces...'
          '  '
        end
      end
    end
  end
end
