using System.Net.Http;
using System.Net.Http.Headers;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Configuration;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Threading.Tasks;
using System;
using System.Text.Json;

namespace oauth_nhsd_api.Pages
{
    [Authorize]
    public class AllergiesModel : PageModel
    {
        public class ParseResponse {
            public string to_ASID { get; set; }
            public string GPConnect_URL { get; set; }
            public string response { get; set; }

        }
        public string ResResponse { get; set; }

        public string ResContent { get; set; }
        public string jsonResponse { get; set; }
        public string resp { get; set; }

        public DateTime SessionExpires { get; set; }

        private readonly IConfiguration _configuration;

        public AllergiesModel(IConfiguration configuration)
        {
            _configuration = configuration;
        }
        public async Task OnGet()
        {

            var tokenAccess = await HttpContext.GetTokenAsync("access_token");
            var tokenRefresh = await HttpContext.GetTokenAsync("refresh_token");
            var tokenExpiresAt = await HttpContext.GetTokenAsync("expires_at");

            HttpRequestMessage req = new HttpRequestMessage(System.Net.Http.HttpMethod.Get,
                _configuration["NHSD:APIEndpoint"] + _configuration["NHSD:NhsNumber"]);

            // make the user restricted request.
            req.Headers.Authorization = new AuthenticationHeaderValue("Bearer", tokenAccess);

            HttpResponseMessage response = await new HttpClient().SendAsync(req);

            // variables created to disply info to the user.
            ResResponse = string.Format("{0} - {1}", (int)response.StatusCode, response.StatusCode);
            ResContent =  response.Content.ReadAsStringAsync().Result;
            ParseResponse jsonResponse =
                JsonSerializer.Deserialize<ParseResponse>(ResContent);
            resp = jsonResponse.response;
            SessionExpires = Convert.ToDateTime(tokenExpiresAt);
        }
    }
}