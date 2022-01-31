/**
 * For this to work add a route like:
 * https://raw.globalsecuritydatabase.org/*	gsd-raw-file
 */

const baseGSD = "https://raw.githubusercontent.com/cloudsecurityalliance/gsd-database/main/"
const statusCode = 302

async function handleRequest(request) {
  const url = new URL(request.url)
  const { pathname } = url

/**
 * GSD ID
 * pathname MUST equal GSD-YYYY-NNNN+
 */

  const GSDIDExtRegExp = new RegExp(/(GSD-[1-2][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]+)$/)

  if (GSDIDExtRegExp.test(pathname)) {
    var IDData = pathname.split("-")
    var DirRegExp = new RegExp(/([0-9][0-9][0-9])$/)
    var dirName = IDData[2].replace(DirRegExp, "xxx");
    const destinationURL = baseGSD + IDData[1] + "/" + dirName + pathname + ".json"
    return Response.redirect(destinationURL, statusCode)
  }

  else {
    const destinationURL = baseGSD + pathname
    return new Response("UNKNOWN DATA please use a valid GSD ID format", { status: 404 })
  }
}

addEventListener("fetch", async event => {
  event.respondWith(handleRequest(event.request))
})
