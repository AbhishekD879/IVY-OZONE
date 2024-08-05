def call(List repositories) {

    //parallel {
        stage ('Fetch application-build ') {
            steps {
                lcgScmGit(repositories[0])
            }
       // }
        /*
        stage ('Fetch Docker Utils') {
            steps {
                lcgScmGit(repoDockerUtils)
            }
        }
        stage ('Fetch application sources') {
            steps {
                lcgScmGit(repoServiceSource)
            }
        }
        */
    }
}
