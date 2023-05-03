# SpamGuard: Spam Detection using Azure Auto ML

**Spam** refers to unsolicited or unwanted electronic messages, typically sent in bulk. These messages can come in various forms, such as emails, text messages, or social media posts, and often contain irrelevant or unwanted content. Spam is important to understand because it can have a negative impact on both individuals and businesses. For individuals, spam can be a nuisance, clogging up inboxes and wasting time. In some cases, spam can even be a security risk, as it may contain malicious links or attachments.

![spam](https://user-images.githubusercontent.com/86774143/229162258-c96256b1-fe6c-4277-9a04-844c5192b32f.jpg)


## 1. Azure Resources
### 1.1 Azure Subscription
In this project we are using **Microsoft Azure Machine Learning** you will need to sign into the Azure Portal at [Microsoft Azure](https://azure.microsoft.com/)  to create the resources. If you are using Azure portal for the first time you can get the subscription from [Free Account](https://azure.microsoft.com/en-us/free/) for free.
### 1.2 Create Azure Resource Group
**Azure resource group** is a logical container in Microsoft Azure that is used to organize and manage related resources. A resource group is a way to group Azure resources such as virtual machines, storage accounts, and virtual networks our project will consist of the Spam data set, compute from training, then compute to run our web service for inferencing.
There are two ways to create an Azure Resource Group.
#### 1.2.1 Create Azure Resource Group - Use Azure Portal
To use the Azure web portal to create the Azure Resource Group follow following steps - [create an Azure Resource Group using portal](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal#create-resource-groups)
#### 1.2.2 Create Azure Resource Group - Use Azure Portal
If you would rather create the Resource Group using bash then you can use [Azure Cloud Shell ](https://learn.microsoft.com/en-us/azure/cloud-shell/overview). Execute the subsequent commands using Azure Cloud Shell (bash):

`Command`
```bash
resourceGroupName=spam$RANDOM-rg
location=SouthCentralUS

az group create \
   --name $resourceGroupName \
   --location $location
```

### 1.3 Create Azure Machine Learning Workspace
[Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/overview-what-is-azure-machine-learning)  is a cloud service for accelerating and managing the machine learning project lifecycle. we can create a model in Azure Machine Learning or use a model built from an open-source platform, such as Pytorch, TensorFlow, or scikit-learn.
There are also two ways to create an Azure Resource Group.
#### 1.3.1 Create Azure Machine Learning Workspace - Use Azure Portal
To create Azure Machine Leaning resource from the Azure portal – [Create Azure Machine Learning Workspace](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace?tabs=python)
#### 1.3.2 Create Azure Resource Group - Use Azure Portal
Execute the subsequent commands using [Azure Cloud Shell ](https://learn.microsoft.com/en-us/azure/cloud-shell/overview) (bash) to create an Azure Machine Learning Workspace:

`Command`
```sh
workspace=spam-$RANDOM

az extension add -n azure-cli-ml

az ml workspace create -w $workspace -g $resourceGroupName  --sku enterprise
```
## 2. Spam Classification with Automated Machine Learning
Using the Azure resources that we have collected now we can use Azure Automated Machine Learnig in the training of best classification model.
### 2.1 Downloading Spam Dataset
First of all we need to download the [Spam Dataset](https://stochasticcoder.files.wordpress.com/2022/04/d9997-smsspamcollection.zip) - this data set came from the University of California Irvine ML Repository. The comma-delimited file that automated ml will use for training is contained in the zip file. Once you've downloaded the file, please unzip it.
### 2.2 Creating an Automated ML Run
Please access your Azure Machine Learning Workspace by clicking on the Azure Resource Group you created in the Azure Portal. I created **spam-17402** using the bash script in this post; yours will have a different name.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/479c9-spam_resource_group-1.png)

Once you have accessed the Machine Learning Resource then click **Launch now** where is says **Try the new Azure Machine Learning studio** towards the center of the screen as the remainder of the post will be using this new UX.

![alt text](https://stochasticcoder.files.wordpress.com/2020/03/0791d-launch_studio.png)

Now you can select Automated ML from the left navigation or choose Automated ML **‘Start Now’**.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/1a8ea-auto_ml_nav.png)

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/d0028-auto_ml_start_now.png)

Once on the Automated ML screen, select **New Automated ML Run**.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/0aab2-new_automl_run.png)

#### 2.2.1 Automated ML Dataset
Now, we will create dataset in our Automated ML run using the database that we have downloaded. Select **Create dataset**, then select **From local files**.

![alt text](https://stochasticcoder.files.wordpress.com/2020/03/17220-create_dataset.png)

Give name and description as this dataset can be used in other models and accessed via the SDK. Select **Browse** and find the downloaded and unzipped spam csv file.

![alt text](https://stochasticcoder.files.wordpress.com/2020/03/61704-datastore_file_selection-1.png)

Moving to the next step after selecting the csv file. Leave the default settings and schema selection:

| Setting | Value |
| ------ | ------ |
| File Format | Delimited|
| Delimeter | Comma |
| Encoding | UTF-8 |
| Column Headers| Use headers from the first file |
| Skip rows | None |

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/60f9c-schema-1.png?w=456&h=293&zoom=2)

#### 2.2.2 Automated ML Compute
As we have added the dataset now we are ready to configure our run. Please make sure to select the dataset you created before configuring your run. Then select **Next**. 

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/eaa29-create_new_auto_ml.png?w=456&h=183&zoom=2)

Give your experiment a descriptive name, such as **spam-experiment**. The dataset's spam column is located in the **Target column** (label). You must build a new compute if this is your first training run with Azure Machine Learning; otherwise, you will have compute options under **Select training cluster**.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/16bc6-configure_run-1.png?w=704&h=346&zoom=2)

Select **Create a new compute** to proceed with a new computer cluster. The name need not be specific to automl because compute can be used for other training runs. You can use the default settings for this post because provisioning the cluster's virtual machines will only take a short while.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/f78ff-automl_compute.png?w=704&h=828&zoom=2)
The next step, Tack Type and Settings, requires you to choose **Classification** as the task type after provisioning your compute and adding it to the run configuration.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/c92bb-classification_task.png?w=704&h=157&zoom=2)

You can modify the run setting by clicking **View additional configuration settings**.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/944d1-view_additional_configs.png)

In this proect, I set an exit score of **0.98** for my run to early terminate when my accuracy reaches 0.98.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/7451b-additional_configs-1.png?w=704&h=661&zoom=2)

Cogratulation - you have successfully completed first **Automated ML Run**.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/d669c-automl_run.png?w=704&h=295&zoom=2)

once your Run is complete, you canview the Visulizations section  for the best model by selecting **Visualizations** or **Matrix**.

![alt text](https://stochasticcoder.files.wordpress.com/2020/03/6021d-visualization.png)

The **Confusion Matrix** for the **Best model** is shown below; It is possible that your matrix looks different.

![alt text](https://stochasticcoder.files.wordpress.com/2020/03/0c658-confusion_matrix-1.png)


## 3. Deploying the ‘Best’ Automated ML Spam Model
### 3.1 Deploy the Best Model
To make downloading and deploying the model easier, automated machine learning will keep track of the best model from all the training runs. With the new Azure Machine Learning studio UX that we introduced in part 2.2 of this project, this is conveniently accessible. Go to your experiment by clicking Experiments on the left navigation, then select your experiment. I labelled mine **"spam-experiment"**, as can be seen below, to deploy your best model.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/f2833-experiments.png)

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/cffd3-spam_experiment.png)

### 3.2 Deployment Configuration
As this is the quickest and easiest way to operate a container in Azure without having to manage any VMs, we will deploy to [Azure Container Instances](https://stochasticcoder.files.wordpress.com/2022/04/d9997-smsspamcollection.zip) (ACI) for this project. Anyone can call your webservice if you leave Enable authentication off. It is important to **Enable Authentication** now.

![alt text](https://stochasticcoder.files.wordpress.com/2020/03/0ab22-deploy_aci_model-1.png)

It will take few minutes to deploy ACI with the docker image and authentication/routing sidecar containers after registering the model and building the docker image. When our endpoint is in a **healthy deployment condition**, as described in the following, the deployment will be finished and ready.


### 3.3 Consuming the Web Service
#### 3.3.1 Web Service Endpoint

Navigate to left navigation menu, to view your deployed enpoint go to **Endpoints**. Select your Endpoint, in my case **spam-detection**.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/a870a-endpoints-1.png)

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/be157-spam_endpoint.png)

Once the **Deployment state** is **Healthy**, the endpoint is prepared for inferencing. As mentioned in this project's section 3.2, this could take a while. The Azure Container Instance resource will also be visible in the newly established Resource Group. (same resource group as Azure Machine learning).

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/35aad-endpoint_details.png)

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/de25c-aci_resource_group_view-1.png)

#### 3.3.2 Consumer Web Service in Python
Here is a straightforward Python example that uses the installed web service to score messages. The Consume area of your spam detection endpoint is where you can find the your **REST endpoint URL** and **Primary** or **Secondary key**.

![alt text](https://stochasticcoder.files.wordpress.com/2022/04/2c4bc-consume_endpoint-1.png)

### Python Code
Paste your endpoint url and key into the following code to score the example messages.
```python
import pandas as pd
import json
import requests

url = 'http://<your url>.azurecontainer.io/score'
key = '<your key>'

spam = {'spam':[1,0,1]}
data = {"data":['PRIVATE! Your 2003 Account Statement for 078','Send me the new number at my work','Free e-book']}

input_data = json.dumps(data)

headers = {'Content-Type':'application/json'}

#for AKS deployment you'd need to the service key in the header as well    
headers = {'Content-Type':'application/json',  'Authorization':('Bearer '+ key)} 

resp = requests.post(uri, input_data, headers=headers)

print("POST to url", uri)
print("input data:", input_data)
print("label:", spam['spam'])
print( resp.text)
```

### Output from PyCharm

```python
input data: {"data": ["PRIVATE! Your 2003 Account Statement for 078", "Send me the new number at my work", "Free e-book"]}
label: [1, 0, 1]
 "{\"result\": [1.0, 0.0, 1.0]}"
```

This program sends a POST request to a machine learning model deployed on Azure Container Instances (ACI) at a specified URL (url). The request includes input data (data) in JSON format.
- The spam variable is a dictionary with a single key spam and a list of binary values representing spam or not spam.
- The input_data variable is the input data in JSON format. It contains a single key data with a list of three strings representing text messages.

Two sets of headers are defined. The first only specifies the content type as JSON. The second set of headers is used when deploying the machine learning model on Azure Kubernetes Service (AKS). It includes the content type and the service key for authentication.
The requests.post() method is called to send the input data to the specified URL with the headers included.

### Importance of Spam Detection
Spam Detection refers to the process of identifying and filtering out unwanted or unsolicited messages, particularly in email communication. Spam messages can include a variety of content, such as advertisements, phishing attempts, malware, and fraudulent schemes.

- Protection against malicious attacks: Spam emails can contain malware, viruses, and phishing attempts that can harm individuals or organizations. Spam detection helps to identify and filter out these malicious emails, reducing the risk of a successful attack.

- Saving time and resources: Spam emails can flood inboxes, wasting time and resources by forcing individuals to sift through irrelevant messages. Spam detection can automatically filter out these emails, allowing individuals to focus on important tasks.

- Avoiding scams: Spam emails often contain scams that can lead to financial loss or identity theft. By detecting and filtering out these emails, individuals and organizations can



