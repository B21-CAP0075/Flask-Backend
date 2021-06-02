#How to Clone this Project

# Deploy to Cloud Run

You can apply this application to the Google Cloud Platform - Cloud Run. Following are the steps for running this application in a Cloud Run environment.

##📌 Set up Google Cloud Platform

**1. Open a Google Cloud Platform account.

If you're new to Google Cloud, you can [create an account](http://console.cloud.google.com/freetrial) and new customers also get $300 in free credits to run, test, and deploy workloads.

**2. In the Google Cloud Console, on the project selector page, select or create a Google Cloud project**

[Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard) to select a project.

**3. Make sure that billing is enabled for your Cloud project**

[learn how to confirm that billing is enabled for your project]
(https://cloud.google.com/billing/docs/how-to/modify-project)

**4. Enable the Cloud SQL Admin API**

[Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=sqladmin.googleapis.com) then select the project used.

***Let the Google Cloud Console tab opened***

**5. Clone the repository and edit the D**
Copy paste this code to clone the repository and change directory into it:

```bash
git clone https://github.com/B21-CAP0075/Flask-Backend.git
cd Flask-Backend
```
See the the file list
```bash
ls
```
This is the file structure of the project
```bash
tree /f /a
```

**6. Containerizing an app and uploading it to Container Registry**

Build your container image using Cloud Build, by running the following command from the directory containing the Dockerfile:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/Flask-Backend
```
where PROJECT-ID is your GCP project ID. You can get it by running 
```bash
gcloud config get-value project
```
***Now you're already create an Image of your project***

**7. Containerizing an app and uploading it to Container Registry**
To deploy the container image:
1. Deploy using the following command (change the PROJECT-ID to your GCP project id):
```bash
gcloud run deploy --image gcr.io/PROJECT-ID/Flask-Backend
```
If prompted to enable the API, Reply y to enable.

Replace PROJECT-ID with your GCP project ID. You can view your project ID by running the command:
```bash
gcloud config get-value project
```
* a. You will be prompted for the service name: press Enter to accept the default name, Flask-Backend
+ b. You will be prompted for region: select the region of your choice, for example us-central1
- c. You will be prompted to allow unauthenticated invocations: respond y

Then wait a few moments until the deployment is complete. On success, the command line displays the service URL.
2. Visit your deployed container by opening the service URL in a web browser.


### This is backend this repository
### Link deploy: https://decare-g2k7tjwhia-uc.a.run.app/
### Predict API: https://decare-g2k7tjwhia-uc.a.run.app/predict
