'use strict()';

var git = require('git-rev-sync'),
  Q = require('q'),
  exec = require('child_process').exec,
  config = {
    port: 3000,
    host: "127.0.0.1"
  },
  fs = require('fs'),
  Logger = require('./lib/logger');

function createEnv(env) {
  var fileContent = "";
  for(var i in env){
    fileContent += i + '=' + env[i] + '\n';
  }
  return fileContent;
}

module.exports = function(grunt) {

  var appConfig = {
    src: 'src',
    dist: 'dist',
    tmp: '.tmp',
    public: 'bma-betstone/public'
  };

	// Load grunt tasks automatically
	require('load-grunt-tasks')(grunt);

	// Time how long tasks take. Can help when optimizing build times
	require('time-grunt')(grunt);

  var publicMethod = {
    buildReport: function(type) {
      var branchDeferred = Q.defer();
      var tagDeferred = Q.defer();
      var commitDeferred = Q.defer();
      var logDeferred = Q.defer();

      function _command (cmd, cb) {
        exec(cmd, { cwd: __dirname }, function (err, stdout) {
          Logger.info('GRUNT', stdout);
          cb(stdout.split('\n').join(''));
        });
      }

      branchDeferred.resolve('Revision branch: ' + git.branch());
      //tagDeferred.resolve('Revision tag: ' + git.tag());
      commitDeferred.resolve('Revision commit: ' + git.long());

      /*var modules = checkTarget(target).split(',');

       modules = invictusAPI.applyDependencies(modules);*/

      return {
        //mainModule: this.getMainModuleName(target),
        //allModules: modules,
        //endpoints: grunt.config.data.ngconstant[type].constants,
        promises: [
          //tagDeferred.promise,
          branchDeferred.promise,
          commitDeferred.promise,
          //logDeferred.promise
        ]
      };
    }
  }

	// Project configuration.
	grunt.initConfig({
    env: grunt.file.readJSON('env.json'),
		pkg: grunt.file.readJSON('package.json'),
		express: {
			options: {
				port: config.port
			},
			dev: {
				options: {
					script: 'keystone.js',
					debug: true
				}
			}
		},

		concurrent: {
			dev: {
				tasks: ['nodemon', 'node-inspector', 'watch'],
				options: {
					logConcurrentOutput: true
				}
			}
		},

		'node-inspector': {
			custom: {
				options: {
					'web-host': 'localhost'
				}
			}
		},

		nodemon: {
			debug: {
				script: 'keystone.js',
				options: {
          cwd: __dirname,
          ignore: ['node_modules/**', 'bma-betstone/node_modules/**'],
					nodeArgs: ['--debug'],
					env: {
						port: config.port
					}
				}
			}
		},

		watch: {
			express: {
				files: [
					'keystone.js',
					'public/js/lib/**/*.{js,json}'
				],
				tasks: ['concurrent:dev']
			},
			livereload: {
				files: [
					'public/styles/**/*.css',
					'public/styles/**/*.less',
					'templates/**/*.jade',
					'bma-betstone/templates/**/*.jade'
				],
				options: {
					livereload: true
				}
			}
		},

    timestamp: 'bmacms_' + new Date().toISOString().replace(/\:/g,'').replace(/\-/g,'').replace(/T/,'_').replace(/\./g,''),

    secret: grunt.file.readJSON('secret.json'),

    sshexec: {
      changeLink: {
        command: 'cd /var/www/projects; rm bma-cms; ' +
          'ln -s <%= timestamp %> bma-cms; ' +
          'ln -s ../bma-cms-env/public <%= timestamp %>/public; ' +
          'ln -s ../bma-cms-env/node_modules <%= timestamp %>/node_modules; ' +
          'ln -s ../../bma-cms-env/bma-betstone/node_modules <%= timestamp %>/bma-betstone/node_modules',
        options: {
          host: '<%= secret.host %>',
          username: '<%= secret.username %>',
          privateKey: grunt.file.read("ssh-keys/id_rsa")
        }
      },
      env: {
        command: 'cp -r /var/www/projects/bma-cms-env/.env /var/www/projects/<%= timestamp %>/.env',
        options: {
          host: '<%= secret.host %>',
          username: '<%= secret.username %>',
          privateKey: grunt.file.read("ssh-keys/id_rsa")
        }
      },
      modules: {
        command: 'cd /var/www/projects/bma-cms-env; npm install; cd /var/www/projects/bma-cms-env/bma-betstone; npm install;',
        options: {
          host: '<%= secret.host %>',
          username: '<%= secret.username %>',
          privateKey: grunt.file.read("ssh-keys/id_rsa")
        }
      },
      restart: {
        command: 'forever stopall; cd /var/www/projects/bma-cms; forever start -m 5 keystone.js',
        options: {
          host: '<%= secret.host %>',
          username: '<%= secret.username %>',
          privateKey: grunt.file.read("ssh-keys/id_rsa")
        }
      },
			runCopyScript: {
				command: 'cd /var/www/projects; ./copyAndRun.sh <%= timestamp %>',
				options: {
					host: '<%= secret.host %>',
					username: '<%= secret.username %>',
					privateKey: grunt.file.read("ssh-keys/id_rsa")
				}
			}
    },

    shell: {
      makeDir: {
        options: {
          stderr: false
        },
        command: 'ssh -i ~/.ssh/id_rsa coralvm.symphony-solutions.eu "cd /var/www/projects; mkdir <%= timestamp %>"'
      },
      copyDev: {
        options: {
          stderr: false,
          maxBuffer: Infinity,
          execOptions: {
            maxBuffer: Infinity
          }
        },
        command: 'chmod 600 ./ssh-keys/id_rsa; ' +
          'scp -rv -i ./ssh-keys/id_rsa dist/* bamboo@coralvm:/var/www/projects/<%= timestamp %>; ' +
          'scp -rv -i ./ssh-keys/id_rsa dist-env/* bamboo@coralvm:/var/www/projects/bma-cms-env'
      },
      archive: {
        options: {
          stderr: false
        },
        command: 'tar -zcf cms_<%= timestamp %>.tar.gz ./dist' // && ' +
          //'tar -zcf cms_env_<%= timestamp %>.tar.gz ./dist-env'
      },
      copyJumpbox: {
        options: {
          stderr: false
        },
        command: 'scp -r ./cms_<%= timestamp %>.tar.gz <%= jumpBoxAddress %>:<%= jumpBoxPath %>/' // && ' +
        /*'scp -r ./cms_env_<%= timestamp %>.tar.gz 10.5.26.133:<%= jumpBoxPath %>' +
          'rm ./cms_<%= timestamp %>.tar.gz && ' +
          'rm ./cms_env_<%= timestamp %>.tar.gz'*/
      },
      unzipCode: {
        options: {
          stderr: false,
          maxBuffer: Infinity,
          execOptions: {
            maxBuffer: Infinity
          }
        },
        command: 'ssh <%= jumpBoxAddress %> "tar -xf <%= jumpBoxPath %>/cms_<%= timestamp %>.tar.gz -C <%= jumpBoxPath %>"'
      },
      unzipEnv: {
        options: {
          stderr: false,
          maxBuffer: Infinity,
          execOptions: {
            maxBuffer: Infinity
          }
        },
        command: 'ssh <%= jumpBoxAddress %> "tar -xf <%= jumpBoxPath %>/cms_env_<%= timestamp %>.tar.gz -C <%= jumpBoxPath %>"'
      },
      runDeploymentScript: {
        options: {
          stderr: false,
	  maxBuffer: Infinity,
	  execOptions: {
	    maxBuffer: Infinity
	  }
        },
        command: 'ssh <%= jumpBoxAddress %> "./rsync.1.sh <%= serverAddress %> <%= jumpBoxPath %> <%= destinationPath %>"'
      },
      moveSources: {
        options: {
          stderr: false,
          maxBuffer: Infinity,
          execOptions: {
            maxBuffer: Infinity
          }
        },
        command: 'ssh <%= jumpBoxAddress %> "cp -R ""'
      },
      renameFolders: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> "ssh giad06t2xzbmaweb01 \"mv /var/www/deployment/dist /var/www/deployment/cms && mv /var/www/deployment/dist-env /var/www/deployment/cms-env \""'
      },
      linkKeystone: {
        options: {
          stderr: false
        },
        command: '<%= jumpBoxAddress %> "ssh giad06t2xzbmaweb01 \"' +
          'ln -s ../dist-env/node_modules /var/www/deployment/dist/node_modules' +
          '\""'
      },
      linkBetstone: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> "ssh giad06t2xzbmaweb01 \"' +
          'ln -s ../../dist-env/bma-betstone/node_modules /var/www/deployment/dist/bma-betstone/node_modules' +
          '\""'
      },
      linkPublic: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> "ssh giad06t2xzbmaweb01 \"' +
          'ln -s ../dist-env/public /var/www/deployment/dist/public' +
          '\""'
      },
      copyEnv: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> "cp -r <%= jumpBoxPath %>/.env <%= jumpBoxPath %>/dist/.env"'
      },
      copyUploads: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> "cp -r <%= jumpBoxPath %>/uploads <%= jumpBoxPath %>/dist/public/images/"'
      },
      archiveFullSource: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> "cd <%= jumpBoxPath %> && tar -zcf ./dist.tar.gz ./dist"'
      },
      foreverConfig: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> \'ssh giad06t2xzbmaweb01 \'' +
          'chmod 755 /var/www/deployment/dist/forever.sh' +
          '\'\''
      },
      foreverExecute: {
        options: {
          stderr: false
        },
        command: 'ssh <%= jumpBoxAddress %> \'ssh giad06t2xzbmaweb01 \'' +
          '/var/www/deployment/dist/forever.sh' +
          '\'\''
      }
    },

    copy: {
      dist: {
        files: [
          {
            expand: true,
            dot: true,
            cwd: '',
            dest: 'dist',
            src: [
              'Procfile',
              'keystone.js',
              'models/**',
              'bma-betstone/**',
              'routes/**',
              'templates/**',
              'updates/**',
              'lib/**'
            ]
          },
          {
            expand: true,
            dot: true,
            cwd: '',
            dest: 'dist-env',
            src: [
              'package.json'
            ]
          },
          {
            expand: true,
            dot: true,
            cwd: '',
            dest: 'dist-env',
            src: [
              'bma-betstone/package.json'
            ]
          },
          // ToDo: should be removed after CDN integration
          {
            expand: true,
            dot: true,
            cwd: '',
            dest: 'dist-env',
            src: [
              'public/**'
            ]
          }
        ]
      },
      distRemote: {
        files: [
          {
            expand: true,
            dot: true,
            cwd: '',
            dest: 'dist',
            src: [
              'Procfile',
              'keystone.js',
              'forever.sh',
              'node.sh',
              'models/**',
              //'node_modules*//**',
              //'bma-betstone/**',
              //'!bma-betstone/node_modules/**',
              'routes/**',
              'templates/**',
              'updates/**',
              'public*//**'
            ]
          }
          /*, {
            expand: true,
            dot: true,
            cwd: '',
            dest: 'dist-env',
            src: [
              'package.json',
              'node_modules*',
              'bma-betstone/package.json',
              'bma-betstone/node_modules*',
              'public*'
            ]
          }*/
        ]
      }
    },

		// Empties folders to start fresh
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            'dist/{,*/}*'
            //'dist-env'
          ]
        }]
      }
    },

    bump: {
      options: {
        files: ['package.json'],
        updateConfigs: [],
        commit: true,
        commitMessage: 'Release v%VERSION%',
        commitFiles: ['package.json'],
        createTag: true,
        tagName: 'v%VERSION%',
        tagMessage: 'Version %VERSION%',
        push: true,
        pushTo: 'origin',
        gitDescribeOptions: '--tags --always --abbrev=1 --dirty=-d',
        globalReplace: false,
        prereleaseName: false,
        regExp: false
      }
    }
	});

  grunt.registerTask('env', function() {
    fs.writeFile(".env", createEnv(grunt.config.get('env'))); 
  });

	// default option to connect server
	grunt.registerTask('serve', function(target) {
		grunt.task.run([
      'env',
      'buildReport',
			'concurrent:dev',
		]);
	});

  // default option to connect server
  grunt.registerTask('build', function(type) {
    if (!type || type === 'dev') {
      grunt.task.run([
        'clean:dist',
        'buildReport',
        'copy:dist'
      ]);
    } else if (type === 'remote') {
      grunt.task.run([
        'clean:dist',
        'buildReport',
        'copy:distRemote'
      ]);
    }
  });

  grunt.registerTask('buildReport', function() {

    var buildReport = publicMethod.buildReport();

    // Add app.version.
    buildReport.appVersion = grunt.file.readJSON('package.json').version;

    Q.allSettled(buildReport.promises)
      .then(function (results) {

        buildReport.cvs = [];

        results.forEach(function (result) {
          if (result.state === 'fulfilled') {
            if(!Array.isArray(result.value)) {
              buildReport.cvs.push(result.value);
            }
            else {
              buildReport.cvsLog = result.value;
            }
          }
        });

        delete buildReport.promises;

        grunt.file.write(appConfig.public + '/dist.json', JSON.stringify(buildReport)); //appConfig.dist + '/
      }).catch(function (error) {
        Logger.error('GRUNT', 'Failed: ' + error);
      });

  });

  /**
   * Deploy build to dev or to staging or to specific remote address.
   *
   * execute 'grunt deploy' or 'grunt deploy:dev' - for deploying on invictus.coral.co.uk
   * execute 'grunt deploy:remote' - for deploying on default staging
   * execute 'grunt deploy:remote:ipAddress' - for deploying on another server
   */
  grunt.registerTask('deploy', function(type, jumpBoxPath, boxAddress, destinationPath, jumpBoxAddress) {
    if (!type || type === 'dev') {
      grunt.log.writeln('[CMS] Deploy build to default dev server');
      grunt.task.run([
        'shell:makeDir',
        'sshexec:env',
        'sshexec:modules',
        'shell:copyDev',
        'sshexec:changeLink',
        //'sshexec:restart',
				'sshexec:runCopyScript'
      ]);
    } else if (type === 'remote') {
      var serverAddress = boxAddress ? boxAddress : 'bm-mobile-tst2';
      var jumpBoxPath = jumpBoxPath ? jumpBoxPath : './tst2';
      var destinationPath = destinationPath ? destinationPath : './';
      var jumpBoxAddress = jumpBoxAddress ? jumpBoxAddress : 'giad00m6xjump29';
      grunt.log.writeln('[CMS log] Deploy build to Jump Box' + ' to folder: "' + jumpBoxPath + '"');
      grunt.config.set('serverAddress', serverAddress);
      grunt.config.set('jumpBoxPath', jumpBoxPath);
      grunt.config.set('destinationPath', destinationPath);
      grunt.config.set('jumpBoxAddress', jumpBoxAddress);
      grunt.task.run([
        'shell:archive',
        'shell:copyJumpbox',
        'shell:unzipCode',
        'shell:copyEnv',
        'shell:copyUploads',
        'shell:archiveFullSource',
        'shell:runDeploymentScript'
      ]);
    }
  });

	grunt.registerTask('server', function () {
		grunt.log.warn('The `server` task has been deprecated. Use `grunt serve` to start a server.');
		grunt.task.run(['serve:' + target]);
	});
};
