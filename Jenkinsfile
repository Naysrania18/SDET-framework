// Same pipeline as GitHub Actions, expressed for Jenkins.
pipeline {
  agent any
  stages {
    stage('Install') { steps { sh 'pip install -r requirements.txt && playwright install chromium' } }
    stage('Smoke')   { steps { sh 'pytest -m smoke -n auto' } }
    stage('Regression') { steps { sh 'pytest -n auto' } }
  }
  post { always { archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true } }
}
