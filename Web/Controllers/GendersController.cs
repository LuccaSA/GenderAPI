using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using GenderAPI.Domain;
using GenderAPI.Web.Models;
using Microsoft.AspNetCore.Mvc;

namespace GenderAPI.Controllers
{
    [Route("api/[controller]")]
    public class GendersController : Controller
    {
        private IGenderService _firstNamesDictionary;

        public GendersController(IGenderService firstNamesDictionary)
        {
            _firstNamesDictionary = firstNamesDictionary;
        }

        // GET api/gender
        [HttpGet]
        public Gender Get(string firstName)
        {
            return new Gender(_firstNamesDictionary, firstName);
        }
    }
}
