lib = File.expand_path('lib', __dir__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'gsd-database'

repo_url = 'https://github.com/cloudsecurityalliance/gsd-tools'

Gem::Specification.new do |s|
  s.version     = GSD.gem_version
  s.platform    = Gem::Platform::RUBY
  s.name        = 'gsd-database'
  s.summary     = 'GSD Database Ruby Interface'
  s.description = 'Provides an easy way to interact with the GSD Database via Ruby.'

  s.required_ruby_version = '>= 3.0.0'

  s.license = 'Apache-2.0'

  s.author   = 'Josh Buker'
  s.email    = 'crypto@joshbuker.com'
  s.homepage = 'https://gsd.id'

  s.files = [
    'lib/gsd-database.rb',
    'lib/gsd/database.rb',
    'lib/gsd/version.rb'
  ]
  s.require_paths = ['lib']

  s.metadata = {
    'bug_tracker_uri'       => "#{repo_url}/issues",
    # 'changelog_uri'         => "#{repo_url}/releases/tag/v#{version}",
    # 'documentation_uri'     => "#{repo_url}/wiki",
    # 'source_code_uri'       => "#{repo_url}/tree/v#{version}",
    'rubygems_mfa_required' => 'true'
  }

  s.add_dependency 'git', '~> 1.0'
end
