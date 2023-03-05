import { Router } from 'itty-router'

const host = 'https://raw.githubusercontent.com/cloudsecurityalliance/gsd-database/main'

// Create a new router
const router = Router()

/**
 * From the Fetch JSON example
 *
 * gatherResponse awaits and returns a response body as a string.
 * Use await gatherResponse(..) in an async function to get the response body
 * @param {Response} response
 */
async function gatherResponse(response) {
  const { headers } = response
  const contentType = headers.get("content-type") || ""
  if (contentType.includes("application/json")) {
    return JSON.stringify(await response.json())
  }
  else if (contentType.includes("application/text")) {
    return response.text()
  }
  else if (contentType.includes("text/html")) {
    return response.text()
  }
  else {
    return response.text()
  }
}

/*
Our index route, a simple hello world.
*/
router.get("/", () => {
  return Response.redirect('https://gsd.id/api', 307);
})

/*
This route demonstrates path parameters, allowing you to extract fragments from the request
URL.

Try visit /example/hello and see the response.
*/
router.get("/:id", async ({ params }) => {
  const identifier = decodeURIComponent(params.id)

  if (!(identifier.match(/^GSD-\d{4}-\d{4,}$/) || identifier.match(/^UVI-\d{4}-\d{4,}$/))) {
    // TODO: Support other ID formats. Also support stripping `.json` if included
    return new Response(
      'Invalid GSD format! Expected something like GSD-2021-1002352.',
      { status: 400 }
    )
  }

  // Split navigation data from identifier
  const year = identifier.split('-')[1]
  const thousands = `${identifier.split('-')[2].slice(0, -3)}xxx`

  // Resolve full url
  const path = `${year}/${thousands}/${identifier}.json`
  const url = `${host}/${path}`

  // From the Fetch JSON example
  const init = {
    headers: {
      "content-type": "application/json;charset=UTF-8",
    },
  }

  const options = {
    headers: {
      "content-type": "application/json;charset=UTF-8",
      "Access-Control-Allow-Origin": "*",
    },
  }

  const response = await fetch(url, init)
  const results = await gatherResponse(response)
  return new Response(results, options)
})

/*
This shows a different HTTP method, a POST.

Try send a POST request using curl or another tool.

Try the below curl command to send JSON:

$ curl -X POST <worker> -H "Content-Type: application/json" -d '{"abc": "def"}'
*/
router.post("/post", async request => {
  // Create a base object with some fields.
  let fields = {
    "asn": request.cf.asn,
    "colo": request.cf.colo
  }

  // If the POST data is JSON then attach it to our response.
  if (request.headers.get("Content-Type") === "application/json") {
    fields["json"] = await request.json()
  }

  // Serialise the JSON to a string.
  const returnData = JSON.stringify(fields, null, 2);

  return new Response(returnData, {
    headers: {
      "Content-Type": "application/json"
    }
  })
})

/*
This is the last route we define, it will match anything that hasn't hit a route we've defined
above, therefore it's useful as a 404 (and avoids us hitting worker exceptions, so make sure to include it!).

Visit any page that doesn't exist (e.g. /foobar) to see it in action.
*/
router.all("*", () => new Response("404, not found!", { status: 404 }))

/*
This snippet ties our worker to the router we deifned above, all incoming requests
are passed to the router where your routes are called and the response is sent.
*/
addEventListener('fetch', (e) => {
  e.respondWith(router.handle(e.request))
})
