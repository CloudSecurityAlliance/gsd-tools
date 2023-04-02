module GSD
  autoload :Database, 'gsd/database'
  autoload :VERSION, 'gsd/version'

  def self.gem_version
    Gem::Version.new VERSION::STRING
  end
end
