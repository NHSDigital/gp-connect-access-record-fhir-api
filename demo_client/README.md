# Example: Web Client & Server App Authenticating with NHS Digital OAuth

This demo client shows how a user could authenticate with NHS Login to retrieve information about their allergies via the [gp-connect-access-record-fhir-api](https://github.com/NHSDigital/gp-connect-access-record-fhir-api)

This demo client is created using this example walkthrough and code [Medium - Example: Web Client & Server App Authenticating with NHS Digital Identity via OAuth](https://aubyncrawford.medium.com/example-web-client-server-app-authenticating-with-nhs-digital-oauth-1563f8c9c5ad)

## Getting Started
This project was created with Visual Studio 2019, and is an ASP.NET Core 3 Web Application.

To run the application:

1. Install .NET SDK 3.1 - see [Install .NET on Windows, Linux, and macOS](https://docs.microsoft.com/en-us/dotnet/core/install/)
2. You will need to set up an account with [NHS Digital API Platform](https://digital.nhs.uk/developer)
3. Create an app on the NHS Digital API Platform and request access to gp-connect-access-record-fhir-api, registering your callback url (`<url of democlient>/callback`)
4. Update `CallbackUrl` in appsettings.json
5. Update the `NhsNumber` in appsettings.json to match that of the NHS Login test user you are using.
6. Enable Secret Manager in the root of the project (demo_client/src/oauth-nhsd-api) - see [Enable secret storage](https://docs.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-6.0&tabs=windows#enable-secret-storage) for instructions.
7. Set up the following secrets: `"secrets:ClientId"` and `"secrets:ClientSecret"` using the credentials provided for your app in the NHS Digital API Platform


## Deployment

This sample can be run locally, as long as it can reach the NHS Digital API Platform

## Built With

* Visual Studio 2019 - ASP.NET Core 3 and Razor pages

## Acknowledgments

* [Medium - Example: Web Client & Server App Authenticating with NHS Digital Identity via OAuth](https://aubyncrawford.medium.com/example-web-client-server-app-authenticating-with-nhs-digital-oauth-1563f8c9c5ad)

