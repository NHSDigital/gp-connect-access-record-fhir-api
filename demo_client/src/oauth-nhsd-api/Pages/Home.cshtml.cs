using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Configuration;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System;


namespace oauth_nhsd_api.Pages
{
    [Authorize]
    public class HomeModel : PageModel
    {
        public string ResResponse { get; set; }

        public string ResContent { get; set; }

        public DateTime SessionExpires { get; set; }

        private readonly IConfiguration _configuration;

        public HomeModel(IConfiguration configuration)
        {
            _configuration = configuration;
        }
        public void OnGet()
        {

        }
    }
}