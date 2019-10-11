## Blog: How to use Transit Gateway to create a single exit point to the internet from multiple VPCs 

### Introduction

The cloudformation and python scripts in this project are intended to be used in support of the AWS blog article here:

The files contained here are as follows:

|File                                    | Description                                                                 |
|----------------------------------------|-----------------------------------------------------------------------------|
|transitgateway-egress-solution.yaml     |The cloudformation template to create the solution in the blog               |
|index.py                                |The python code to update VPC route tables                                   |
|crhelper.py                             |Some additional python code to help with logging runtime info to cloudwatch  |
|requirements.txt                        |The libraries required by the python code, including all dependencies        |

The cloudformation automatically creates the solution highlighted in the blog, and the python code will populate the VPC route table with the correct routes after creation of the transit gateway attachments, as that function is not yet supported within cloudformation.

The python code is intended to be run as a lambda custom resource, called by the cloudformation template. In order to create the package for the custom resource, you will need to zip up the two python files here (index.py and crhelper.py) along with the libraries that are imported by that code. 

These libraries are listed within the requirements.txt file, which can be used as part of a pip install to create the entire package.

### How to create the lambda package

For the uninitiated, here is what i did to create the lambda package:

1. I made sure that python was up to date on my mac. I'm guessing you can google how to do that!
2. I installed a python virtual environment on my mac. If you know how to do that, great! If you don't then go have a look here https://virtualenv.pypa.io/en/latest/
3. I downloaded the `requirements.txt` file into my current working folder
4. I created a target folder `./<folder_name>`
5. I downloaded the two python files and moved them into the target folder
6. I created a virtual environment, using the command `virtualenv venv`
7. I started that environment, using the command `source venv/bin/activate`. This just makes sure you are installing libraries into a clean environment, rather than depending on anything that is already installed on your laptop.
8. I then put all the libraries I needed into the target folder, using the command `pip install -r requirements.txt -t <./folder_name>`
9. Now for a cleanup. I deactivated the virtual environment using the command `deactivate` and then deleted the folder venv that had been created in my working directory.
10. Lastly, I zipped up the contents of the target folder ready to deploy to an S3 bucket. It's really important that you don't zip the target folder, but rather, go into the target folder, and then zip everything from inside it. I did this using the commands 
```
cd <folder_name>
zip -r <lambda-package-name>.zip *
mv <lambda-package-name>.zip ..
cd ..
```
11. I was then left with my working folder that had a `requirements.txt` file, a `<lambda-package-name>.zip` file, and a `<folder_name>` folder.

### Running the cloudformation template

Once you have created the lambda package, you need to upload it to an S3 bucket in the same region as you want to deploy the cloudformation template. You then need to go into the template, and edit the S3 bucket name and lambda package name defined in the parameters, or just type the correct values in at the prompt when running the template. 

This should then create the entire environment, update the VPC route tables and be ready for you to play with.

### How I tested the deployed environment

For testing, I just created a linux instance in each of the app subnets, and also one in the public egress subnet. This public one, i gave a public as well as private IP address, so i could ssh in. I then created the appropriate security groups so that ssh and ICMP were permitted, and proved that i could ping and ssh between all the instances.

  
## License

This library is licensed under the MIT-0 License. See the LICENSE file.

