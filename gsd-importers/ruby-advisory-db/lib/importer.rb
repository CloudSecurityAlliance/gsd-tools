# Debugging tools
require 'byebug'
require 'diffy'

require_relative 'advisory'
require 'bundler/audit/database'
require 'gsd-database'

puts "Checking if RubySec Database exists..."

if Bundler::Audit::Database.exists?
  puts "Exists, updating to latest..."
  Bundler::Audit::Database.update!
else
  puts "Does not exist, downloading..."
  Bundler::Audit::Database.download
end

GIT_REPO = 'https://github.com/cloudsecurityalliance/gsd-database.git'
GIT_FORK = ENV.fetch('GSD_DATABASE_FORK', GIT_REPO)
GSD_DATABASE_PATH = ENV.fetch(
  'GSD_DATABASE_PATH',
  File.expand_path(File.join(Gem.user_home,'.local','share','gsd-database'))
)

puts "Syncing GSD Database (this may take a while)..."
gsd_database = GSD::Database.new(
  work_branch: 'automated/ruby-advisory-db',
  git_repo: GIT_REPO,
  git_fork: GIT_FORK,
  repo_path: GSD_DATABASE_PATH
)
gsd_database.sync!

NAMESPACE = 'github.com/rubysec/ruby-advisory-db'

puts "Parsing advisories..."

rubysec_database = Bundler::Audit::Database.new
rubysec_database.send(:each_advisory_path) do |path|
  advisory = GSD::RubySecImporter::Advisory.new(yaml_file: path)

  if advisory.invalid?
    puts "Invalid entry, skipping"
    next
  end

  gsd_file_path = File.join(gsd_database.repo_path, advisory.gsd_file_path)

  puts "Checking #{advisory.gsd_id}"

  gsd_database.modify(gsd_file_path) do |gsd_entry|
    gsd_entry['namespaces'] = {} if gsd_entry['namespaces'].nil?
    gsd_entry['namespaces'][NAMESPACE] = advisory.to_h.compact

    gsd_entry['gsd'] = {} if gsd_entry['gsd'].nil?
    gsd_entry['gsd']['osvSchema'] = advisory.to_osv if gsd_entry['gsd']['osvSchema'].nil?
  end
end

puts "Saving changes to branch"
gsd_database.save!

puts "Pushing to fork under #{gsd_database.work_branch}"
gsd_database.push!

puts "Done!"
