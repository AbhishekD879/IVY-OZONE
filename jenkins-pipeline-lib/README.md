# README #

Pipeline Shared Library

### What is this repository for? ###

* Quick summary
  
    Sharable libraries available to any Pipeline jobs running on Jenkins environment
    
* Version
  
* [Documentation](https://jenkins.io/doc/book/pipeline/shared-libraries/#defining-shared-libraries)


* Please use pattern below for naming groovy global var/function convention using Camel style

  
  libraryId Type Description .groovy
  
   libraryId - Library owner 
       lcg      - Ladbrokes Coral Group
       example  - examples 
       
   Type - type of global var/function
       
       Common
       AppBuild
       Aws
       Scm
       Deploy
       CodeQuality
       AgentDocker
       Notify
       
   Description - additional information

*  Misc
   IDE  Visual Studio Code + Jenkins plugin

* Deploy type
    
    nginx
            nginxRsync              - distribution -> direct delivery in consecutive by rsync ->  destination server
            nginxJumpRsync          - distribution -> Jump host -> delivery in consecutive by rsync -> destination server    
        
    akamai
            akamaiRsync             - distribution -> direct delivery in consecutive by rsync -> destination server          
            akamaiRsyncParallel     - distribution -> direct delivery in parallel mode by rsync -> destination server       
            akamaiCms               - distribution -> direct delivery in consecutive by cms -> destination server
            akamaiCmsParallel       - distribution -> direct delivery in parallel mode by cms -> destination server  
            
    Function name convention:
        
        [Destination Service][Route][Tool][Thread]
        
        Destination Service     - akamai, nginx, docker
        Route                   - Direct as default, Jump
        Tool                    - Rsync, Cms, Ansible 
        Thread                  - Consecutive as default, Parallel 
