/*
  Extracts any envvars that are prefixed with the GSD_ namespace
  so they can be overlayed a top the dotenv base configuration in
  <project root> .env

  This file is loaded during the quasar.config.js which is not transpiled
  by babel so this module is define to be require nodejs style.

  Normally this would extend quasar boot but since this targets a browser
  dotenv requires node fs, os, and path which are unavailable.
*/

let envConfig = Object.keys(process.env)
  .reduce((result, key) => {
    key.startsWith('GSD_') ? result[key] = process.env[key] : {}
    return result
  }, {});

dotEnv = require('dotenv').config().parsed
envConfig = Object.assign({}, dotEnv, envConfig)

exports = envConfig
