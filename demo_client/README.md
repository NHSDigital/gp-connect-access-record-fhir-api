# Example: Web Client & Server App Authenticating with NHS Digital OAuth

This demo client shows how a user could authenticate with NHS Login to retrieve information about their allergies via the [gp-connect-access-record-fhir-api](https://github.com/NHSDigital/gp-connect-access-record-fhir-api)

This demo client is created using this example walkthrough and code [Medium - Example: Web Client & Server App Authenticating with NHS Digital Identity via OAuth](https://aubyncrawford.medium.com/example-web-client-server-app-authenticating-with-nhs-digital-oauth-1563f8c9c5ad)

## Getting Started
This project was created with Visual Studio 2019, and is an ASP.NET Core 5.0 Web Application.

### Setting up a NHS Digital App for login
1. You will need to set up an account with [NHS Digital API Platform](https://digital.nhs.uk/developer)
2. Create an app on the NHS Digital API Platform and request access to gp-connect-access-record-fhir-api, registering your callback url `http://localhost:5000/callback`

This will generate a Client Key and a Client Secret, these will be used to authenticate later so make note of them.
### Running Latest Release
To run the application without any dependancies on your machine, follow these steps:

1. Visit and Download the latest release for your Operating system from [Download Latest Release](https://github.com/NHSDigital/gp-connect-access-record-fhir-api/releases)
2. Unzip the folder
3. From your terminal, navigate to the unzipped folder
4. To run the application run the following command:
    * Windows: `start oauth-nhsd-api.exe ClientId="<your_client_key>" ClientSecret="<your_secret_key>"`
    * Linux: `./oauth-nhsd-api --urls http://+:5000 ClientId="<your_client_key>" ClientSecret="<your_secret_key>"`
    * Mac `./oauth-nhsd-api ClientId="<your_client_key>" ClientSecret="<your_secret_key>"`
    
       Note: MacOS will complain about security stuff, you need to allow apps from identified developers on System Preferences -> Allow apps downloaded from: -> App Store and identified developers.

### To Run Locally
To run the application:

1. Install .NET SDK 5.0 - see [Install .NET on Windows, Linux, and macOS](https://docs.microsoft.com/en-us/dotnet/core/install/)
2. Navigate to gp-connect-access-record-fhir-api\demo_client\src\oauth-nhsd-api\ 
3. Update the `NhsNumber` in appsettings.json to match that of the NHS Login test user you are using.
4. Run
```
dotnet run .\oauth-nhsd-api.csproj ClientId="PLACE_CLIENT_KEY_HERE" ClientSecret="PLACE_CLIENT_SECRET_HERE"
```
5. Navigate to http://localhost:5000 on your browser


### Running with Docker
To run the application using docker:

1. Install the latest version of [Make](http://gnuwin32.sourceforge.net/packages/make.htm) and [Docker](https://docs.docker.com/desktop/)
2. Navigate to gp-connect-access-record-fhir-api\demo_client\src\oauth-nhsd-api\
3. Create a file named ".env", with contents:
```
CLIENT_ID=PLACE_CLIENT_KEY_HERE
CLIENT_SECRET=PLACE_CLIENT_SECRET_HERE
```
4. Run `make build`
5. Run `make run`
6. Navigate to http://localhost:5000 on your browser


## Deployment

This sample can be run locally, as long as it can reach the NHS Digital API Platform

## Built With

* Visual Studio 2019 - ASP.NET Core 5.0 and Razor pages

## Acknowledgments

* [Medium - Example: Web Client & Server App Authenticating with NHS Digital Identity via OAuth](https://aubyncrawford.medium.com/example-web-client-server-app-authenticating-with-nhs-digital-oauth-1563f8c9c5ad)

