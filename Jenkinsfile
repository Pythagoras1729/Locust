pipeline{
    agent any
    parameters{
        string(name: 'NO_OF_USERS', defaultValue: '', description:'Number of users')
        string(name: 'HATCH_RATE', defaultValue: '', description: 'Hatch rate')
        string(name: 'E2E_50_THRESHOLD', defaultValue: '0', description: 'e2e .50 threshold ms')
        string(name: 'E2E_90_THRESHOLD', defaultValue: '0', description: 'e2e .90 threshold ms')
        string(name: 'E2E_99_THRESHOLD', defaultValue: '0', description: 'e2e .99 threshold ms')
        string(name: 'SERVER', defaultValue: '', description: 'Name ofServer we want to test')
        string(name: 'API_METHOD', defaultValue:'', description:'(GET, PUT, POST)')
        string(name: 'RUN_TIME', defautValue:'',description:'Write X-hours Y-minutes Z-seconds as XhYmZs')
    }
    stages{
        stage('Set Environment'){
            steps{
                script{
                    env.PATH="C:\\WINDOWS\\SYSTEM32;"+env.PATH             
                }
            }
        }
        stage('run test'){
            steps{
                script{
                    println("Test starts")
                        def cmd= "python  Locust/main.py \
                                       -No_of_Users ${NO_OF_USERS} \
                                       -Hatch_Rate ${HATCH_RATE}   \
                                       -E2e_50_threshold ${E2E_50_THRESHOLD} \
                                       -E2e_90_threshold  ${E2E_90_THRESHOLD} \
                                       -E2e_99_threshold ${E2E_99_THRESHOLD} \
                                       -Server ${SERVER} \
                                       -Api_Method ${API_METHOD} \
                                       -Run_Time ${RUN_TIME}"
                        bat """                               
                                ${cmd}
                           """
                }//end of script
            }//end of steps
        }//end of stage
    }//end of stages
    post{
        success{
                archiveArtifacts '*/*/*/*.csv'
        }//end of success
    }//end of post
}//end of pipeine
