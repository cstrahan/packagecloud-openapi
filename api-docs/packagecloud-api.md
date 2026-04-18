- [Sign up](/users/new)
- [Login](/session/new)

# API Docs

REST API for automation of common tasks for debian, rpm, rubygems, and python packages.

<a id="getting_started"></a>

## Getting Started

<a id="important_info"></a>

### Important Info

Before getting started there are a handful of important things to know:

1. All API requests **must** be made over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure). There is no plain-text HTTP support.
2. Most API requests are authenticated using an API token. API tokens are supplied to the API via [HTTP basic authentication](http://en.wikipedia.org/wiki/Basic_access_authentication). Provide your API token as the username and leave the password empty. The APIs which are not authenicated in this way will be marked explicitly as so below.
3. The API is versioned. This document describes v1 and the URLs start with https://packagecloud.io/api/v1/.

<a id="response_codes"></a>

### HTTP Response Codes

HTTP Response codes returned by the API:

- 200 OK
   An API request was successfully processed.
- 201 Created
   An API request was successfully processed and a new resource was created.
- 401 Unauthorized
   The username and password are incorrect or when the API token used for a request is invalid.
- 404 Not Found
   The specified API resource was not found.
- 422 Unprocessable Entity
   A parameter to the API was provided but was unexpected, malformed, not supported, or otherwise invalid. The response will be a JSON object mapping the erroneous field name to error message(s).

Error responses have a JSON body with a human readable string with a more detailed error explanation.

<a id="clientlibs"></a>

### API Client Libraries

Our client libraries are open sourced on our GitHub account. We gladly accept pull requests and appreciate any issues being filed against the GitHub repositories.

#### Ruby

<https://github.com/computology/packagecloud-ruby>

#### Java

<https://github.com/computology/io.packagecloud.client>

#### Go

<https://github.com/mlafeldt/pkgcloud>

<https://github.com/edwarnicke/pkgcloud>

<a id="pagination"></a>

### Pagination

Any endpoint returning a list of things (like the [Search](#resource_packages_method_search), [Versions](#resource_packages_method_versions) and [Packages API](#resource_packages_method_index))
uses the following headers for pagination information:

- `Link:` Links for the next, previous and last page, according to the
  proposed [RFC-5988](http://tools.ietf.org/html/rfc5988) standard for Web linking.
  *Example:*
   `Link:
       <https://packagecloud.io/api/v1/repos/julio/test/packages.json?page=5>;
  rel="last",
       <https://packagecloud.io/api/v1/repos/julio/test/packages.json?page=2>; rel="next"`
- `Total:` How many items exist in the total collection.
- `Per-Page:` How many items are rendered in this response.
- `Max-Per-Page:` Maximum number of items that can be returned per page.

Note: pass a `?per_page` parameter to restrict how many items are returned per page. Default is 30.
Any `per_page` parameter greater than `Max-Per-Page` will be ignored and the maximum set of items allowed per page will be returned instead.

<a id="api_tokens"></a>

## API Tokens

<a id="api_tokens"></a>

In order to interact with the API, you will need to first obtain your access token. If you [login](/login), your token will appear on this page.

All API requests must contain a valid API token in the username field of [HTTP basic authentication](http://en.wikipedia.org/wiki/Basic_access_authentication). For example, a request to the distributions endpoint would look like this:

```
curl https://somevalidapitoken:@packagecloud.io/api/v1/distributions
```

A request with a missing or invalid API token will result in a 401 Unauthorized response.

This token can also be retrieved programmatically via an API request which must be authenticated with your the email address and password associated with your packagecloud account.

To retrieve your token programmatically, you can make the following API call:

```
GET https://email:password@packagecloud.io/api/v1/token.json
```

An example CURL request:

```
curl "https://hi%40hi.com:Asdd45VvaarT4591@packagecloud.io/api/v1/token.json"
```

Parameters:

- `email` must be your packagecloud account email address.
- `password` must be your packagecloud password

Be sure to [URL encode](http://en.wikipedia.org/wiki/Percent-encoding#Percent-encoding_reserved_characters) your username and password.

<a id="api_tokens_responses"></a>

### Responses

If successful, you will receive **200 OK** response and the response body will be JSON hash mapping the key *token* to your API token.

An example response:

```
{"token":"f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0"}
```

You will use this API token for making all other API requests.

If unsuccessful, you will receive **401 Unauthorized** and the error response body will be a JSON hash containing the key error whose value is a string describing the error in more detail.

An example error response:

```
{"error":"Unauthenticated"}
```

<a id="resource_distributions"></a>

## distributions

<a id="resource_distributions_method_index"></a>

### index

```
GET /api/v1/distributions
```

#### Response:

`Hash<String, Distribution>` The response will be a JSON hash with the keys "deb", "dsc", and "rpm" whose values will be an array of hashes describing each distribution. This distribution hash will have an key called "versions" whose value is an array of JSON hashes describing each version of a particular Linux distribution which supports the package type.

#### Example request(s):

```
curl https://packagecloud.io/api/v1/distributions.json
```

#### Example response:

```
{
  "deb": [
      {
          "display_name": "Ubuntu",
          "index_name": "ubuntu",
          "versions": [
              {
                  "id": 4,
                  "display_name": "5.10 Breezy Badger",
                  "index_name": "breezy"
              },
              {
                  "id": 5,
                  "display_name": "6.06 LTS Dapper Drake",
                  "index_name": "dapper"
              },
              {
                  "id": 6,
                  "display_name": "6.10 Edgy Eft",
                  "index_name": "edgy"
              }
          ]
      },
      {
          "display_name": "Debian",
          "index_name": "debian",
          "versions": [
              {
                  "id": 22,
                  "display_name": "4.0 etch",
                  "index_name": "etch"
              }

          ]
       }

  ]
}
```

<a id="resource_gpg_keys"></a>

## gpg\_keys

<a id="resource_gpg_keys_method_index"></a>

### index

List gpg keys for a repository.

```
GET /api/v1/repos/:user_id/:repo/gpg_keys.json
```

#### Response:

`Array<GPGKey>` An array of GPG key objects that belong to this repository.

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos/username/reponame/gpg_keys.json
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "gpg_keys" : [
     {
        "self" : "/api/v1/repos/username/reponame/gpg_keys/username-reponame-85D7FBF915DFCBC6.pub.gpg.json",
        "download_url" : "https://packagecloud.io/username/reponame/gpgkey/username-reopname-85D7FBF915DFCBC6.pub.gpg",
        "keytype" : "repo",
        "destroy_url" : "/api/v1/repos/username/reponame/gpg_keys/username-reponame-85D7FBF915DFCBC6.pub.gpg.json",
        "fingerprint" : "26F67F3E5E89BB30DCD7AC6E85D7FBF915DFCBC6",
        "name" : "username-reponame-85D7FBF915DFCBC6.pub.gpg"
     }
  ]
}
```

<a id="resource_gpg_keys_method_create"></a>

### create

Create a GPG key.

```
POST /api/v1/repos/:user_id/:repo/gpg_keys.json
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `gpg_key[keydata]` `String` The GPG key file to use when creating a key.

#### Response:

[GPGKey](#object_GPGKey) The newly created GPG key object.

#### Example request(s):

```
curl -X POST -F "gpg_key[keydata]=@/path/to/key.gpg" https://packagecloud.io/api/v1/repos/username/reponame/gpg_keys.json
```

#### Example response:

```
{
   "self" : "/api/v1/repos/username/reponame/gpg_keys/username-reopname-85D7FBF915DFCBC6.pub.gpg.json",
   "download_url" : "https://packagecloud.io/username/reponame/gpgkey/username-reopname-85D7FBF915DFCBC6.pub.gpg",
   "fingerprint" : "26F67F3E5E89BB30DCD7AC6E85D7FBF915DFCBC6",
   "keytype" : "package",
   "name" : "username-reponame-85D7FBF915DFCBC6.pub.gpg",
   "destroy_url" : "/api/v1/repos/username/reponame/gpg_keys/username-reponame-85D7FBF915DFCBC6.pub.gpg.json"
}
```

<a id="resource_gpg_keys_method_destroy"></a>

### destroy

Destroy a GPG key

```
DELETE /api/v1/repos/:user_id/:repo/gpg_keys/:keyname.json
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:keyname` `String` The GPG Key keyname to delete

#### Example request(s):

```
curl -X DELETE https://packagecloud.io/api/v1/repos/username/reponame/gpg_keys/username-reponame-85D7FBF915DFCBC6.pub.gpg.json
```

#### Example response:

```
< HTTP/1.1 204 OK
```

<a id="resource_gpg_keys_method_show"></a>

### show

View a single GPG Key

```
GET /api/v1/repos/:user_id/:repo/gpg_keys/:keyname.json
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:keyname` `String` The GPG Key keyname.

#### Response:

<GPGKey> The GPG Key object representing the requested key.

#### Example request(s):

```
curl -X GET https://packagecloud.io/api/v1/repos/username/reponame/gpg_keys/username-reponame-85D7FBF915DFCBC6.pub.gpg.json
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
   "self" : "/api/v1/repos/username/reponame/gpg_keys/username-reopname-85D7FBF915DFCBC6.pub.gpg.json",
   "download_url" : "https://packagecloud.io/username/reponame/gpgkey/username-reopname-85D7FBF915DFCBC6.pub.gpg",
   "fingerprint" : "26F67F3E5E89BB30DCD7AC6E85D7FBF915DFCBC6",
   "keytype" : "package",
   "name" : "username-reponame-85D7FBF915DFCBC6.pub.gpg",
   "destroy_url" : "/api/v1/repos/username/reponame/gpg_keys/username-reponame-85D7FBF915DFCBC6.pub.gpg.json"
}
```

<a id="resource_licenses"></a>

## licenses

<a id="resource_licenses_method_index"></a>

### index

STILL IN USE BY GITLAB
Retrieve a packagecloud:enterprise license file and GPG signature.
Signature can be verified with the packagecloud GPG key:
<https://packagecloud.io/gpg.key>.

```
GET /api/v1/licenses/:license_key/license.json
```

#### URL Params:

- `:license_key` `String` The packagecloud:enterprise license key

#### Response:

`Hash` JSON hash containing the license data and GPG signature

#### Example request(s):

```
curl https://packagecloud.io/api/v1/licenses/aabbccddeeffaa/license.json
```

#### Example response:

```
< HTTP/1.0 200 OK
```

```
{
  "license": "---\n:company_name: company-2\n:company_domain:
  www.domain2.com\n:user_email: joe3@joe.com\n:user_max:
  -1\n:repository_max: -1\n:token_max: -1\n:apt: true\n:yum:
  true\n:rubygem: true\n:start_date: \n:end_date: \n",
  "signature": "-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG
      v1.4.11
      (GNU/Linux)\n\niQIcBAABAgAGBQJU2DiPAAoJEB/spSUmciijLT4P/0PFZSJigrm8vzEM6xmfo2OD\neS16BgN/neF0UGAoysMmfO0bTETk9l4ow4xn2eKLLQ7h0aXYoX7Rz/GD/YKu67UQ\nHor8j61jabFVHBwiZjWQsmQfoJRFkAW4eG1bAfTy/PeUpVt9crYv/IMe7cLCk/Ki\nQlRZuj/uoAHSMZsl1zsr1gGHCGoEaX3sVwtmYOsn7GvyJ+MnYqNET4qGV9WXxSCj\nwNC2IjPH6KBcUZO6YZ6hUW3wCwxtRKIaq+H6qtVPpQbMYvPRKax1h8jEbzl1NqmL\n6YyAu/Xuf80JZQ19cW6SswaU8eSxpCWdfC8Pnx3ocpQMVnzNhJp/vbSJUKSsLO2V\nGhBW0nPBLJ4LWvt3mqtnrpNntyt5NHNJSMXc8ODEiLMd9oxn68g7yWmKqH28yD2n\nOEG4IhvTg+NruO1tRr5ENGeqR/SsagFbH0qNpTInaYVq/OJj34+9nPO7Br09698D\nWPjvkfoiScyz9k8wH8vpA524ckL1+WMEfpf/84nmwlFUOJR7L7J5jE5UVDkk3px1\nmcZeOlsiNUSK5nn3UURtSxnwF87t7FyJPcTiK78ZqHPje1JTv78y0ZZnyrRNa7D4\n/m5TSCwHwu150ioPHAUXzUwzj1Rx/DVOEUscqtau62usirjmjU3eJkWUXS37tOwt\nMk1Bmnzaij2d8LglcvYV\n=ZmwX\n-----END PGP SIGNATURE-----\n"
}
```

<a id="resource_master_tokens"></a>

## master\_tokens

<a id="resource_master_tokens_method_index"></a>

### index

List master tokens for a repo.

```
GET /api/v1/repos/:user_id/:repo/master_tokens
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.

#### Response:

`Array<MasterToken>` An array of master token objects that belong to this repository.

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos/username/reponame/master_tokens
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[{
   "value" : "e5480f5b38f1f78de2aaa0fa732d1427b1b83113371fd97d",
   "name" : "default",
   "read_tokens" : [
      {
         "value" : "3fe453060fd7f017219e308eb98ccf273b4c3655ba57577a",
         "name" : "app1.someservice.com"
      }
   ],
   "paths" : {
      "self" : "/api/v1/repos/username/reponame/master_tokens/1"
   }
}]
```

<a id="resource_master_tokens_method_search"></a>

### search

Search for master tokens

###### Note:

Default is 30 per page, see response headers for [pagination](#pagination) information.

```
GET /api/v1/repos/:user_id/:repo/master_tokens/search
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.

#### Query Params:

- `:q` `String` The name of the MasterToken.

#### Response:

`Array<MasterTokensResult>` An array of {MasterTokensResult} objects for this search query.

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos/username/reponame/master_tokens/search?q=prod
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[{
   "name" : "production",
   "value" : "e5480f5b38f1f78de2aaa0fa732d1427b1b83113371fd97d",
   "self_url": "/api/v1/repos/username/reponame/master_tokens/1"
   "read_tokens_url" : "/api/v1/repos/username/reponame/master_tokens/1/read_tokens"
}]
```

<a id="resource_master_tokens_method_show"></a>

### show

Show a master token.

```
GET /api/v1/repos/:user_id/:repo/master_tokens/:id
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:id` `Integer` The id or value of the MasterToken.

#### Response:

`Array` The name and value of the master token and API path for associated Read Tokens

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos/username/reponame/master_tokens/1
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[{
   "value" : "e5480f5b38f1f78de2aaa0fa732d1427b1b83113371fd97d",
   "name" : "default",
   "read_tokens_url" : "/api/v1/repos/username/reponame/master_tokens/1/read_tokens"
}]
```

<a id="resource_master_tokens_method_create"></a>

### create

Create a master token.

```
POST /api/v1/repos/:user_id/:repo/master_tokens
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `master_token[name]` `String` The name of the token to create.

#### Response:

[MasterToken](#object_MasterToken) The newly created master token

#### Example request(s):

```
curl -X POST -F "master_token[name]=app_servers" https://packagecloud.io/api/v1/repos/username/reponame/master_tokens
```

#### Example response:

```
< HTTP/1.1 201 Created
```

```
{
    "value" : "1f3311f78de2aaa0fa732d1427b1b83113371fd97d",
    "name" : "app_servers",
    "paths" : {
        "self" : "/api/v1/repos/username/reponame/master_tokens/1"
    }
}
```

<a id="resource_master_tokens_method_destroy"></a>

### destroy

Destroy a master token and all of its read token children.

NOTE: Default tokens have their token value rotated when used with this
API. All private repositories must have default master tokens.

```
DELETE /api/v1/repos/:user_id/:repo/master_tokens/:id
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:id` `Integer` The id of the master token to be destroyed.

#### Example request(s):

```
curl -X DELETE https://packagecloud.io/api/v1/repos/username/reponame/master_tokens/1
```

#### Example response:

```
< HTTP/1.1 204 OK
```

<a id="resource_packages"></a>

## packages

<a id="resource_packages_method_contents"></a>

### contents

Inspect the contents of a debian source package.

```
POST /api/v1/repos/:user_id/:repo/packages/contents.json
```

#### URL Params:

- `package[distro_version_id]` `Integer` The id of the DistroVersion to push this package to. Get this from the distributions endpoint.
- `package[package_file]` `File` The `.dsc` file to inspect the contents of.

#### Response:

`PackageContents` A JSON object with a `files` key containing an array of files referenced in this source package.

#### Example request(s):

```
curl -X POST                                                  \
     -F "package[distro_version_id]=17"                       \
     -F "package[package_file]=@path/to/jake_1.0-7.dsc"             \
        "https://packagecloud.io/api/v1/repos/test_user/test_repo/packages/contents.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "files": [
    {
      "filename": "jake_1.0.orig.tar.bz2",
      "size": 1108,
      "md5sum": "a7a309b55424198ee98abcb8092d7be0"
    },
    {
      "filename": "jake_1.0-7.debian.tar.gz",
      "size": 1571,
      "md5sum": "0fa5395e95ddf846b419e96575ce8044"
    }
  ]
}
```

<a id="resource_packages_method_create"></a>

### create

Push a package.

NOTE: that for Deban .dsc packages, you must upload each of the files contained in the .dsc.
You can use the package\_contents API to determine the filename, md5sum, and size of the files referenced by the DSC.
All other package types (debian, rpm, python, and java) need only specify the distro\_version\_id and package\_file parameters.

```
POST /api/v1/repos/:user_id/:repo/packages.json
```

#### URL Params:

- `package[distro_version_id]` `Integer` The id of the DistroVersion to push this package to. Get this from the distributions endpoint. Not required for rubygems.
- `package[package_file]` `File` The package file.
- `package[source_files][]` `Array<File>` For debian source packages only: the source files that are specified in the .dsc.
- `package[coordinates]` `String` For Maven/Java/Android packages only: the coordinates of this artifact if they cannot be computed from metadata within the package.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package.

#### Example request(s):

```
curl -X POST https://packagecloud.io/api/v1/repos/test_user/test_repo/packages.json \
     -F "package[distro_version_id]=48"     \
     -F "package[package_file]=@path/to/jake-1.0-1.el6.x86_64.rpm"
```

#### Example response:

```
< HTTP/1.1 201 Created
```

```
{
  "name": "jake",
  "distro_version": "fedora/22",
  "architecture": "x86_64",
  "repository": "test_repo",
  "size": "3712",
  "summary": "jake douglas is a very nice young man.",
  "filename": "jake-1.0-1.el6.x86_64.rpm",
  "description": "as it so happens, jake douglas is a very nice young man.",
  "dependencies": [
    {
      "context": "requires",
      "dependencies": [
        "libc.so.6(GLIBC_2.2.5)(64bit)",
        "rtld(GNU_HASH)"
      ]
    }
  ],
  "md5sum": "5abe922fc4bbf5bbdac9b85173371892",
  "sha1sum": "062fd41ecf96587309ec9a3ae2035cc44c348b8f",
  "sha256sum": "070da5370a96ba3ae679e7d02d7de6309e4d159340d9f3b555d6d5b4b7cf260a",
  "sha512sum": "406fa288d5dfff194ec2b119b798c4658375a5d07b34f2d6350885cdf6b620f3fdeee45427fef8bcd37e6624049fba0c633b5b4030b79bf96028db6b4f01de87",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T02:49:29.000Z",
  "licenses": [
    "GPL"
  ],
  "version": "1.0",
  "release": "1.el6",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm/download",
  "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "self_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json"
}
```

#### Example request(s):

```
curl -X POST \
     -F "package[distro_version_id]=17"     \
     -F "package[package_file]=@path/to/jake_1.0-7.dsc"  \
     -F "package[source_files][]=@path/to/jake_1.0-7.debian.tar.gz" \
     -F "package[source_files][]=@path/to/jake_1.0.orig.tar.bz2" \
        "https://packagecloud.io/api/v1/repos/test_user/test_repo/packages.json"
```

#### Example response:

```
< HTTP/1.1 201 Created
```

```
{
  "name": "jake",
  "distro_version": "ubuntu/xenial",
  "architecture": "i386 amd64 all",
  "repository": "test_repo",
  "size": "3732.0",
  "summary": null,
  "filename": "jake_1.0-7.dsc",
  "description": null,
  "dependencies": [
    {
      "context": "build-depends",
      "dependencies": [
        "pkg-config",
        "quilt"
      ]
    },
    {
      "context": "build-depends-indep",
      "dependencies": [
        "debhelper (>= 2.0.40)",
        "gettext",
        "bzip2",
        "cpio"
      ]
    }
  ],
  "md5sum": null,
  "sha1sum": null,
  "sha256sum": null,
  "sha512sum": null,
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-14T14:35:33.598Z",
  "licenses": [],
  "version": "1.0",
  "release": "7",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7.dsc/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7.dsc/download",
  "package_html_url": "/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7.dsc",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7.dsc",
  "self_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7.json"
}
```

#### Example request(s):

```
curl -X POST \
     -F "package[distro_version_id]=17"     \
     -F "package[package_file]=@../packages/java/mylibrary.jar"  \
     -F "package[coordinates]=com.packagecloud:mylibrary:1.0" \
        "https://packagecloud.io/api/v1/repos/user/repo/packages.json"
```

#### Example response:

```
< HTTP/1.1 201 Created
```

```
{
  "package": {
    "version": "1.0",
    "filename": mylibrary-1.0.jar,
    "size": 100.0,
    "distro_version_id": 22,
    "created_at": "2016-01-07T19:12:48.346Z"
  }
}
```

<a id="resource_packages_method_promote"></a>

### promote

Promote a package.

```
POST /api/v1/repos/:user_id/:repo/:distro/:version/:package/promote.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:distro` `String` The name of the distribution the package is in. (i.e. ubuntu)
- `:version` `String` The version name of the distribution the package is in. (i.e. precise)
- `:package` `String` The full name of the package.
- `:destination` `String` The fully qualified repository name (e.g., "user/repo") to move the package.

#### Query Params:

- `:scope` `String` The scope of the Node.JS package to promote. Only required if the package to promote is scoped. Include the escaped '@' (i.e. ?scope=%40example).

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package.

#### Example request(s):

###### Notes:

This API is similar to a move operation. Once this API call completes
successfull, the package being promoted will only exist in the
destination.

Upon successful completion of this API, download statistics for the package being moved will be cleared.

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `jake-1.0-3.el6.x86_64.rpm` on Enterprise Linux 7,

from user/example-repo to julio/testrepo:

```
curl -X POST                                \
     -F "destination=julio/testrepo"        \
     "https://packagecloud.io/api/v1/repos/user/example-repo/el/7/jake-1.0-3.el6.x86_64.rpm/promote.json"
```

#### Example response:

RPM Package

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jake",
  "distro_version": "fedora/22",
  "architecture": "x86_64",
  "repository": "test_repo",
  "size": "3712",
  "summary": "jake douglas is a very nice young man.",
  "filename": "jake-1.0-1.el6.x86_64.rpm",
  "description": "as it so happens, jake douglas is a very nice young man.",
  "dependencies": [
    {
      "context": "requires",
      "dependencies": [
        "libc.so.6(GLIBC_2.2.5)(64bit)",
        "rtld(GNU_HASH)"
      ]
    }
  ],
  "md5sum": "5abe922fc4bbf5bbdac9b85173371892",
  "sha1sum": "062fd41ecf96587309ec9a3ae2035cc44c348b8f",
  "sha256sum": "070da5370a96ba3ae679e7d02d7de6309e4d159340d9f3b555d6d5b4b7cf260a",
  "sha512sum": "406fa288d5dfff194ec2b119b798c4658375a5d07b34f2d6350885cdf6b620f3fdeee45427fef8bcd37e6624049fba0c633b5b4030b79bf96028db6b4f01de87",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T02:49:29.000Z",
  "licenses": [
    "GPL"
  ],
  "version": "1.0",
  "release": "1.el6",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm/download",
  "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "self_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json"
}
```

#### Note:

The `dependencies` array for Debian packages will list dependencies for the following contexts: `depends`, `recommends`, `suggests`, `enhances`, `pre-depends`

#### Example request(s):

Deb Package

##### For `packagecloud-test1.1-2amd64.deb` on Ubuntu

Xenial, from test*user/test*repo to armando/promote\_test:

```
curl -X POST                                \
     -F "destination=armando/promote_test"          \
     "https://packagecloud.io/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7_amd64.deb/promote.json"
```

#### Example response:

Deb Package

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jake",
  "distro_version": "ubuntu/xenial",
  "architecture": "amd64",
  "repository": "test_repo",
  "size": "3290",
  "summary": null,
  "filename": "jake_1.0-7_amd64.deb",
  "description": "На берегу пустынных волн",
  "dependencies": [
    {
      "context": "depends",
      "dependencies": [
        "dpkg (>= 1.15.4) | install-info",
        "libc6 (>= 2.4)"
      ]
    },
    {
      "context": "suggests",
      "dependencies": [
        "indent"
      ]
    }
  ],
  "md5sum": "8d47647f97d78e6bd4428afa93e67d76",
  "sha1sum": "ce1c52b7d1a4abc44e54a3f4bab28b9f92b5bc06",
  "sha256sum": "84ce72ad3627539f15176f16004f6ed95bed4efcbe5f591bf3e0c50031826892",
  "sha512sum": "f4c99e53490bd98ee3cd57224a5d0a3bf351d1ddc160cff56d1736a06db80c40d28ac104009cc76dbdaab7beb65a07cb6b712ad3d8bb3471d8bd289fd3d5570e",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T23:55:14.000Z",
  "licenses": [],
  "version": "1.0",
  "release": "7",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7_amd64.deb/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7_amd64.deb/download",
  "package_html_url": "/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7_amd64.deb",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7_amd64.deb",
  "self_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7.json"
}
```

#### Note:

The `dependencies` array for Debian Source packages (DSC) will list dependencies for the following contexts: `build-depends` and `build-depends-indep`

#### Example request(s):

DSC Package

##### For `jake_1.0-7.dsc` on Ubuntu

Trusty, from test*repo/test*repo to armando/promote\_test:

```
curl -X POST                                \
     -F "destination=armando/promote_test"          \
     "https://packagecloud.io/api/v1/repos/test_user/test_repo/ubuntu/trusty/jake_1.0-7.dsc/promote.json"
```

#### Example response:

DSC Package

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jake",
  "distro_version": "ubuntu/xenial",
  "architecture": "amd64",
  "repository": "test_repo",
  "size": "3290",
  "summary": null,
  "filename": "jake_1.0-7_amd64.deb",
  "description": "На берегу пустынных волн",
  "dependencies": [
    {
      "context": "depends",
      "dependencies": [
        "dpkg (>= 1.15.4) | install-info",
        "libc6 (>= 2.4)"
      ]
    },
    {
      "context": "suggests",
      "dependencies": [
        "indent"
      ]
    }
  ],
  "md5sum": "8d47647f97d78e6bd4428afa93e67d76",
  "sha1sum": "ce1c52b7d1a4abc44e54a3f4bab28b9f92b5bc06",
  "sha256sum": "84ce72ad3627539f15176f16004f6ed95bed4efcbe5f591bf3e0c50031826892",
  "sha512sum": "f4c99e53490bd98ee3cd57224a5d0a3bf351d1ddc160cff56d1736a06db80c40d28ac104009cc76dbdaab7beb65a07cb6b712ad3d8bb3471d8bd289fd3d5570e",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T23:55:14.000Z",
  "licenses": [],
  "version": "1.0",
  "release": "7",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7_amd64.deb/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7_amd64.deb/download",
  "package_html_url": "/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7_amd64.deb",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7_amd64.deb",
  "self_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7.json"
}
```

#### Note:

The `dependencies` array for Node.js packages will list dependencies for the following contexts: `dependencies`, `devDependencies`,
`optionalDependencies`, `bundleDependencies`, and `peerDependencies`.

#### Example request(s):

Node.js package

##### For `packagecloud-test-1.1.1.tgz`, from test*user/test*repo to armando/promote\_test:

```
curl -X POST
     -F "destination=armando/promote_test"
     "https://packagecloud.io/api/v1/repos/test_user/test_repo/node/1/packagecloud-test-1.1.1.tgz/promote.json"
```

#### Example response:

Node.js package

```
< HTTP/1.1 200 OK
```

```
{
   "destroy_url" : "/api/v1/repos/armando/promote_test/node/1/packagecloud-test-1.1.1.tgz",
   "filename" : "packagecloud-test-1.1.1.tgz",
   "md5sum" : "06ecacb6acb089c7880069197b24a3fd",
   "promote_url" : "/api/v1/repos/armando/promote_test/node/1/packagecloud-test-1.1.1.tgz/promote.json",
   "sha256sum" : "69f75883d3b46afde2d4d6f1385115f85ddbe36e3c0c6947ffe3c1b642e527f7",
   "package_url" : "/api/v1/repos/armando/promote_test/package/node/packagecloud-test/1.1.1.json",
   "epoch" : null,
   "downloads_detail_url" : "/api/v1/repos/armando/promote_test/package/node/packagecloud-test/1.1.1/stats/downloads/detail.json",
   "repository" : "test_repo",
   "repository_url" : "/api/v1/repos/armando/promote_test",
   "repository_html_url" : "/armando/promote_test",
   "private" : false,
   "version" : "1.0.0",
   "versions_url" : "/api/v1/repos/armando/promote_test/package/node/packagecloud-test/versions.json",
   "summary" : null,
   "downloads_count_url" : "/api/v1/repos/armando/promote_test/package/node/packagecloud-test/1.1.1/stats/downloads/count.json",
   "indexed" : false,
   "self_url" : "/api/v1/repos/armando/promote_test/package/node/packagecloud-test/1.1.1.json",
   "created_at" : "2017-12-22T16:54:01.000Z",
   "licenses" : null,
   "size" : "385",
   "description" : "A test package for testing",
   "uploader_name" : "joe",
   "release" : null,
   "distro_version" : "node/1",
   "package_html_url" : "/armando/promote_test/packages/node/packagecloud-test-1.1.1.tgz",
   "sha1sum" : "a19643dcfa74fde00f02c00bc77c77db0a30b4d5",
   "downloads_series_url" : "/api/v1/repos/armando/promote_test/package/node/packagecloud-test/1.1.1/stats/downloads/series/daily.json",
   "name" : "packagecloud-test",
   "total_downloads_count" : 0,
   "dependencies" : [],
   "sha512sum" : "95cf2124ee4aa2d45e9ace6558b2ccd9875a6400ed557cbff4bd88669aa5b301ecdcabc45654b754d8c1fcaafac938683f600b3dd4802398a96399edf18612ee",
   "scope" : null,
   "download_url" : "https://packagecloud.io/armando/promote_test/packages/node/packagecloud-test-1.1.1.tgz/download",
   "architecture" : null
}
```

#### Note:

The `dependencies` array for Node.js packages will list dependencies for the following contexts: `dependencies`, `devDependencies`,
`optionalDependencies`, `bundleDependencies`, and `peerDependencies`.

#### Example request(s):

Scoped Node.js package

##### For `@scope/packagecloud-test-1.1.1.tgz`, from test*user/test*repo to armando/promote\_test:

```
curl -X POST
     -F "destination=armando/promote_test"
     "https://packagecloud.io/api/v1/repos/test_user/test_repo/node/1/packagecloud-test-1.1.1.tgz/promote.json?scope=%40scope"
```

#### Example response:

Node.js package

```
< HTTP/1.1 200 OK
```

```
{
   "destroy_url" : "/api/v1/repos/armando/promote_test/node/1/packagecloud-test-1.1.1.tgz?scope=%40scope",
   "filename" : "packagecloud-test-1.1.1.tgz",
   "md5sum" : "06ecacb6acb089c7880069197b24a3fd",
   "promote_url" : "/api/v1/repos/armando/promote_test/node/1/packagecloud-test-1.1.1.tgz/promote.json?scope=%40scope",
   "sha256sum" : "69f75883d3b46afde2d4d6f1385115f85ddbe36e3c0c6947ffe3c1b642e527f7",
   "package_url" : "/api/v1/repos/armando/promote_test/package/node/@scope%2fpackagecloud-test/1.1.1.json",
   "epoch" : null,
   "downloads_detail_url" : "/api/v1/repos/armando/promote_test/package/node/@scope%2fpackagecloud-test/1.1.1/stats/downloads/detail.json",
   "repository" : "test_repo",
   "repository_url" : "/api/v1/repos/armando/promote_test",
   "repository_html_url" : "/armando/promote_test",
   "private" : false,
   "version" : "1.0.0",
   "versions_url" : "/api/v1/repos/armando/promote_test/package/node/@scope%2fpackagecloud-test/versions.json",
   "summary" : null,
   "downloads_count_url" : "/api/v1/repos/armando/promote_test/package/node/@scope%2fpackagecloud-test/1.1.1/stats/downloads/count.json",
   "indexed" : false,
   "self_url" : "/api/v1/repos/armando/promote_test/package/node/@scope%2fpackagecloud-test/1.1.1.json",
   "created_at" : "2017-12-22T16:54:01.000Z",
   "licenses" : null,
   "size" : "385",
   "description" : "A test package for testing",
   "uploader_name" : "joe",
   "release" : null,
   "distro_version" : "node/1",
   "package_html_url" : "/armando/promote_test/packages/node/packagecloud-test-1.1.1.tgz?scope=%40scope",
   "sha1sum" : "a19643dcfa74fde00f02c00bc77c77db0a30b4d5",
   "downloads_series_url" : "/api/v1/repos/armando/promote_test/package/node/@scope%2fpackagecloud-test/1.1.1/stats/downloads/series/daily.json",
   "name" : "packagecloud-test",
   "total_downloads_count" : 0,
   "dependencies" : [],
   "sha512sum" : "95cf2124ee4aa2d45e9ace6558b2ccd9875a6400ed557cbff4bd88669aa5b301ecdcabc45654b754d8c1fcaafac938683f600b3dd4802398a96399edf18612ee",
   "scope" : null,
   "download_url" : "https://packagecloud.io/armando/promote_test/packages/node/packagecloud-test-1.1.1.tgz/download?scope=%40scope",
   "architecture" : null
}
```

<a id="resource_packages_method_show"></a>

### show

Show Package

```
GET /api/v1/repos/:user_id/:repo/package/:type/:distro/:version/:package/:arch/:package_version/:release.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:type` `String` The type of package it is, "rpm" or "deb".
- `:distro` `String` The name of the distribution the package is in. (i.e. ubuntu)
- `:version` `String` The version name of the distribution the package is in. (i.e. precise)
- `:package` `String` The name of the package.
- `:arch` `String` The architecture of the package. (note: debs use amd64 while rpms use x86\_64 for arch)
- `:package_version` `String` The version (without epoch) of the package.

#### Query Params:

- `:release` `String` The release, if the package contains one.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package.

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `jake-1.0-3.el6.x86_64.rpm` on Enterprise Linux 7:

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json"
```

#### Example response:

RPM Package

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jake",
  "distro_version": "fedora/22",
  "architecture": "x86_64",
  "repository": "test_repo",
  "size": "3712",
  "summary": "jake douglas is a very nice young man.",
  "filename": "jake-1.0-1.el6.x86_64.rpm",
  "description": "as it so happens, jake douglas is a very nice young man.",
  "dependencies": [
    {
      "context": "requires",
      "dependencies": [
        "libc.so.6(GLIBC_2.2.5)(64bit)",
        "rtld(GNU_HASH)"
      ]
    }
  ],
  "md5sum": "5abe922fc4bbf5bbdac9b85173371892",
  "sha1sum": "062fd41ecf96587309ec9a3ae2035cc44c348b8f",
  "sha256sum": "070da5370a96ba3ae679e7d02d7de6309e4d159340d9f3b555d6d5b4b7cf260a",
  "sha512sum": "406fa288d5dfff194ec2b119b798c4658375a5d07b34f2d6350885cdf6b620f3fdeee45427fef8bcd37e6624049fba0c633b5b4030b79bf96028db6b4f01de87",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T02:49:29.000Z",
  "licenses": [
    "GPL"
  ],
  "version": "1.0",
  "release": "1.el6",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm/download",
  "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "self_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json"
}
```

#### Note:

The `dependencies` array for RPM packages will list all `Requires` and `PreReq` values under the context `requires`

#### Example request(s):

Deb Package

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7.json"
```

#### Example response:

Deb Package

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jake",
  "distro_version": "ubuntu/xenial",
  "architecture": "amd64",
  "repository": "test_repo",
  "size": "3290",
  "summary": null,
  "filename": "jake_1.0-7_amd64.deb",
  "description": "На берегу пустынных волн",
  "dependencies": [
    {
      "context": "depends",
      "dependencies": [
        "dpkg (>= 1.15.4) | install-info",
        "libc6 (>= 2.4)"
      ]
    },
    {
      "context": "suggests",
      "dependencies": [
        "indent"
      ]
    }
  ],
  "md5sum": "8d47647f97d78e6bd4428afa93e67d76",
  "sha1sum": "ce1c52b7d1a4abc44e54a3f4bab28b9f92b5bc06",
  "sha256sum": "84ce72ad3627539f15176f16004f6ed95bed4efcbe5f591bf3e0c50031826892",
  "sha512sum": "f4c99e53490bd98ee3cd57224a5d0a3bf351d1ddc160cff56d1736a06db80c40d28ac104009cc76dbdaab7beb65a07cb6b712ad3d8bb3471d8bd289fd3d5570e",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T23:55:14.000Z",
  "licenses": [],
  "version": "1.0",
  "release": "7",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7_amd64.deb/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7_amd64.deb/download",
  "package_html_url": "/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7_amd64.deb",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7_amd64.deb",
  "self_url": "/api/v1/repos/test_user/test_repo/package/deb/ubuntu/xenial/jake/amd64/1.0-7.json"
 }
```

#### Note:

The `dependencies` array for Debian packages will list dependencies for the following contexts: `depends`, `recommends`, `suggests`, `enhances`, `pre-depends`

#### Example request(s):

DSC Package

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7.json"
```

#### Example response:

DSC Package

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jake",
  "distro_version": "ubuntu/xenial",
  "architecture": "i386 amd64 all",
  "repository": "test_repo",
  "size": "3732.0",
  "summary": null,
  "filename": "jake_1.0-7.dsc",
  "description": null,
  "dependencies": [
    {
      "context": "build-depends",
      "dependencies": [
        "pkg-config",
        "quilt"
      ]
    },
    {
      "context": "build-depends-indep",
      "dependencies": [
        "debhelper (>= 2.0.40)",
        "gettext",
        "bzip2",
        "cpio"
      ]
    }
  ],
  "md5sum": null,
  "sha1sum": null,
  "sha256sum": null,
  "sha512sum": null,
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-14T14:35:33.598Z",
  "licenses": [],
  "version": "1.0",
  "release": "7",
  "epoch": 0,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7.dsc/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7.dsc/download",
  "package_html_url": "/test_user/test_repo/packages/ubuntu/xenial/jake_1.0-7.dsc",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/ubuntu/xenial/jake_1.0-7.dsc",
  "self_url": "/api/v1/repos/test_user/test_repo/package/dsc/ubuntu/xenial/jake/i386%20amd64%20all/1.0-7.json"
}
```

#### Note:

The `dependencies` array for Debian Source packages (DSC) will list dependencies for the following contexts: `build-depends` and `build-depends-indep`

<a id="resource_packages_method_anyfile_show"></a>

### anyfile\_show

Show Anyfile Package

```
GET /api/v1/repos/:user_id/:repo/package/anyfile/:package/:version.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package.
- `:version` `String` The version of the package.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Anyfile Version API](#resource_packages_method_anyfile_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `packagecloud-test-0.1.asc`:

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.6.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "name": "hello",
  "distro_version": "anyfile/1",
  "architecture": null,
  "repository": "test_repo",
  "size": "659",
  "summary": null,
  "filename": "hello-0.0.6.asc",
  "description": "null",
  "dependencies": null,
  "md5sum": "63f15a3efcf982d610b0376aae0a40fe",
  "sha1sum": "0080db94bb9b3fbfae2ae2c9a720d5cf7a724bbc",
  "sha256sum": "f101e1f32d7e4863c3e983b3709fe1755a34a8f45184ef507868267c23f76f0e",
  "sha512sum": "b50259b470eb609688fd99b30db7e6664e5bf3e47e43266a34e321b928b8c687dc11e9d461d4eb980697a17bb96a8cde197ea755396e25a831d78deeab696061",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-14T15:58:49.000Z",
  "licenses": null,
  "version": "0.0.6",
  "release": null,
  "epoch": null,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.6.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/anyfile/1/hello-0.0.6.asc/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/anyfile/hello-0.0.6.asc/download?distro_version_id=129",
  "package_html_url": "/test_user/test_repo/packages/anyfile/hello-0.0.6.asc",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.6/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/anyfile/anyfile/hello/0.0.6/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.6/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/anyfile/1/hello-0.0.6.asc",
  "self_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.6.json"
}
```

<a id="resource_packages_method_gem_show"></a>

### gem\_show

Show RubyGem Package

```
GET /api/v1/repos/:user_id/:repo/package/gem/:package/:version.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package.
- `:version` `String` The version of the package.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [RubyGem Versions API](#resource_packages_method_gem_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `jakedotrb-0.0.1.gem`:

```
curl "https://packagecloud.io/api/v1/repos/julio/testrepo/package/gem/jakedotrb/0.0.1.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jakedotrb",
  "distro_version": "RubyGem",
  "architecture": null,
  "repository": "test_repo",
  "size": "3072",
  "summary": "helping people learn about my friend jake douglas.",
  "filename": "jakedotrb-0.0.1.gem",
  "description": "helping people learn about my friend jake douglas.",
  "dependencies": null,
  "md5sum": "448024a4ac0b6244659c707cfa070df6",
  "sha1sum": "c4365658774d8c259885471acb6cc659caca16b9",
  "sha256sum": "1897be32375d4fc3337df00930ab94afbdfeb26545492127bdbe7fe05e7e1e9d",
  "sha512sum": "27f6286aa047a5c1dd5c7c80e1cf1eccc8ca9c8a61a17cc552277d0d6d745275523fa6cdac610d6a6abb9091509241de447b673e84ead83947f3378641e11217",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-14T14:31:16.000Z",
  "licenses": [
    "MIT"
  ],
  "version": "0.0.1",
  "release": null,
  "epoch": null,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/gems/jakedotrb-0.0.1.gem/download",
  "package_html_url": "/test_user/test_repo/packages/gems/jakedotrb-0.0.1.gem",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem",
  "self_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1.json"
}
```

#### Note:

The `dependencies` array for RubyGem packages will list dependencies for the following contexts: `runtime` and `development`

<a id="resource_packages_method_python_show"></a>

### python\_show

Show Python Package

```
GET /api/v1/repos/:user_id/:repo/package/python/:package/:version.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package.
- `:version` `String` The version of the package.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Python Version API](#resource_packages_method_python_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `jake-1.2-py3-none-any.whl`:

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "name": "packagecloud-test",
  "distro_version": "python",
  "architecture": null,
  "repository": "test_repo",
  "size": "3128",
  "summary": "A sample Python project",
  "filename": "packagecloud_test-0.9.7b1-py2.py3-none-any.whl",
  "description": "A sample Python project for pushing to packagecloud",
  "dependencies": null,
  "md5sum": "a47e28fef7602f51f296a533eb081fff",
  "sha1sum": "25416aa58f9a5e7a6be23e084c6cbfdd392ab3b2",
  "sha256sum": "f114202a20cacaf3a0de65752a3ae9da963047567323ce2fedaeb8a5b0f7fe63",
  "sha512sum": "592aecff82aaf416eed0c038b83c71c9e9f85a2300437636dec0a4ffcf813a3b82eb1c0cbcbbbc61f1d784da6ad3609de4e313c2bbcff46b2b6eaf29197d1fe7",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-14T15:58:49.000Z",
  "licenses": null,
  "version": "0.9.7b1",
  "release": null,
  "epoch": null,
  "indexed": false,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/python/1/packagecloud_test-0.9.7b1-py2.py3-none-any.whl/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/python/packagecloud_test-0.9.7b1-py2.py3-none-any.whl/download",
  "package_html_url": "/test_user/test_repo/packages/python/packagecloud_test-0.9.7b1-py2.py3-none-any.whl",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/python/1/packagecloud_test-0.9.7b1-py2.py3-none-any.whl",
  "self_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1.json"
}
```

#### Note:

The `dependencies` array for Python packages will list dependencies for the following contexts: `requires`, `requires-dist`, `requires-external`, `requires-extra`, and `requires-python`

<a id="resource_packages_method_java_show"></a>

### java\_show

Show Java Package

```
GET /api/v1/repos/:user_id/:repo/package/java/maven2/:package/:version.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package.
- `:version` `String` The version of the package.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Python Versions API](#resource_packages_method_python_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `jake-2.3.jar`:

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/java/maven2/io.packagecloud/jake/2.3.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "name": "jake",
  "distro_version": "java/maven2",
  "architecture": null,
  "repository": "test_repo",
  "size": "2404",
  "summary": null,
  "filename": "jake-2.3.jar",
  "description": null,
  "dependencies": [
    {
      "context": "test",
      "dependencies": [
        "junit.junit 3.8.1"
      ]
    }
  ],
  "md5sum": null,
  "sha1sum": null,
  "sha256sum": null,
  "sha512sum": null,
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T23:54:48.000Z",
  "licenses": null,
  "version": "2.3",
  "release": null,
  "epoch": null,
  "indexed": true,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/java/maven2/io.packagecloud/jake/2.3.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/java/maven2/io.packagecloud/jake/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/java/maven2/io.packagecloud/jake-2.3.jar/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/java/jake-2.3.jar/artifacts/jake-2.3.jar/download"
  "package_html_url": "/test_user/test_repo/packages/java/jake-2.3.jar",
  "downloads_detail_url": "N/A",
  "downloads_series_url": "N/A",
  "downloads_count_url": "N/A",
  "destroy_url": "/api/v1/repos/test_user/test_repo/java/maven2/io.packagecloud/jake-2.3.jar",
  "self_url": "/api/v1/repos/test_user/test_repo/package/java/maven2/io.packagecloud/jake/2.3.json"
}
```

<a id="resource_packages_method_helm_show"></a>

### helm\_show

Show Helm Package

```
GET /api/v1/repos/:user_id/:repo/package/helm/:index_name/:package/:version.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:index_name` `String` The version of helm index
- `:package` `String` The name of the package.
- `:version` `String` The version of the package.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Helm Version API](#resource_packages_method_helm_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `hello-kubernetes-2.0.0.tgz`:

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/helm/v1/hello-kubernetes/2.0.0.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "name": "hello-kubernetes",
  "distro_version": "helm/v1",
  "architecture": null,
  "repository": "test_repo",
  "size": "1877",
  "summary": "A sample Helm chart",
  "filename": "hello-kubernetes-2.0.0.tgz.",
  "description": "A sample Helm chart",
  "dependencies": [],
  "md5sum": "797df36c5c713768cf660b6d29895ca6",
  "sha1sum": "4f6bab7bd2f6da189506f2e11032b46945dd74b0",
  "sha256sum": "52d7800b708cb3c96493accf9b15e8bceba9ac31a3fbbe6fde9f176e503bddbe",
  "sha512sum": "dbfe5a1bdf9d7fb4b9cfbff373526fc840d68cce19b17000d751223af21f3a1de1d6230458b14d57eb96eb19a9ab1390542f9081849b0f606870984a7a5fb06c",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-14T15:58:49.000Z",
  "licenses": null,
  "version": "2.0.0",
  "release": null,
  "epoch": null,
  "indexed": true,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/helm/v1/hello-kubernetes/2.0.0.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/helm/v1/hello-kubernetes/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/helm/v1/hello-kubernetes-2.0.0.tgz/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/helm/v1/hello-kubernetes-2.0.0.tgz/download?distro_version_id=140",
  "package_html_url": "/test_user/test_repo/packages/helm/v1/hello-kubernetes-2.0.0.tgz",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/helm/v1/hello-kubernetes/2.0.0/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/helm/v1/hello-kubernetes/2.0.0/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/helm/v1/hello-kubernetes/2.0.0/stats/downloads/count.jsom",
  "destroy_url": "/api/v1/repos/test_user/test_repo/helm/v1/hello-kubernetes-2.0.0.tgz",
  "self_url": "/api/v1/repos/test_user/test_repo/package/helm/v1/hello-kubernetes/2.0.0.json"
}
```

<a id="resource_packages_method_versions"></a>

### versions

List Package Versions

```
GET /api/v1/repos/:user_id/:repo/package/:type/:distro/:version/:package/:arch/versions.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:type` `String` The type of package it is, "rpm" or "deb".
- `:distro` `String` The name of the distribution the package is in. (i.e. ubuntu)
- `:version` `String` The version name of the distribution the package is in. (i.e. precise)
- `:package` `String` The name of the package.
- `:arch` `String` The architecture of the package. (note: debs use amd64 while rpms use x86\_64 for arch)

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of all the versions for this package

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/versions.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "jake",
    "distro_version": "fedora/22",
    "created_at": "2017-03-13T02:49:29.000Z",
    "version": "1.0",
    "release": "1.el6",
    "epoch": 0,
    "private": false,
    "type": "rpm",
    "filename": "jake-1.0-1.el6.x86_64.rpm",
    "uploader_name": "test_user",
    "indexed": false,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm"
  }
]
```

<a id="resource_packages_method_gem_versions"></a>

### gem\_versions

List RubyGem Package Versions

```
GET /api/v1/repos/:user_id/:repo/package/gem/:package/versions.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package.

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of all the versions for this package.

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/versions.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "jakedotrb",
    "distro_version": "RubyGem",
    "created_at": "2017-03-14T14:31:16.000Z",
    "version": "0.0.1",
    "release": null,
    "epoch": null,
    "private": false,
    "type": "gem",
    "filename": "jakedotrb-0.0.1.gem",
    "uploader_name": "test_user",
    "indexed": false,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1.json",
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/gems/jakedotrb-0.0.1.gem",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/gems/jakedotrb-0.0.1.gem/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem"
  }
]
```

<a id="resource_packages_method_node_show"></a>

### node\_show

Show Node.js Package

```
GET /api/v1/repos/:user_id/:repo/package/node/:package/:version.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package. If this is a scoped package, the name should include an @ and an escaped '/' (e.g., @scope%2Fpkg-name).
- `:version` `String` The version of the package.

#### Response:

[PackageDetails](#object_PackageDetails) A JSON object representing the package

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Node.js Versions API](#resource_packages_method_node_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

##### For `test-pkg-1.3.1.tgz`:

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
  "name": "test-pkg",
  "distro_version": "node/1",
  "architecture": null,
  "repository": "test_repo",
  "size": "691",
  "summary": null,
  "filename": "test-pkg-1.3.1.tgz",
  "description": "test description",
  "dependencies": [
    {
      "context": "dependency",
      "dependencies": [
        "express"
      ]
    },
    {
      "context": "peerDependency",
      "dependencies": [
        "tea"
      ]
    }
  ],
  "md5sum": "b7037cbf8a54d73eeef32f9e73d2139e",
  "sha1sum": "6be6783461d5d3a57d56a0c87388bf42c04c1b55",
  "sha256sum": "d71e85ca552011c6f811bc176e799bd777f4608c6a5f268b326ab95613145eeb",
  "sha512sum": "3e9f904bedeaa3c4dd461570f7c788e3a53783176c39ca16f2f40852777fad24980bcda567ea142f731a4def2bc659d6f021526c08aed76e512194515c2af829",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-12-19T03:11:21.000Z",
  "licenses": null,
  "version": "1.3.1",
  "release": null,
  "epoch": null,
  "indexed": true,
  "scope": null,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/node/1/test-pkg-1.3.1.tgz/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/node/test-pkg-1.3.1.tgz/download",
  "package_html_url": "/test_user/test_repo/packages/node/test-pkg-1.3.1.tgz",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/node/1/test-pkg-1.3.1.tgz",
  "self_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1.json"
}
```

#### Note:

The `dependencies` array for Node.js packages will list dependencies for the following contexts: `dependencies`, `devDependencies`,
`optionalDependencies`, `bundleDependencies`, and `peerDependencies`.

<a id="resource_packages_method_node_versions"></a>

### node\_versions

List Node.js Package Versions

```
GET /api/v1/repos/:user_id/:repo/package/node/:package/versions.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package. If this is a scoped package, the name should include an @ and an escaped '/' (e.g., @scope%2Fpkg-name).

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of all the versions for this package.

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/node/test-pkg/versions.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "test-pkg",
    "distro_version": "node/1",
    "created_at": "2017-12-19T03:11:21.000Z",
    "version": "1.3.1",
    "release": null,
    "epoch": null,
    "scope": null,
    "private": false,
    "type": "node",
    "filename": "test-pkg-1.3.1.tgz",
    "uploader_name": "test_user",
    "indexed": true,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1.json",
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/node/test-pkg/1.3.1/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/node/test-pkg-1.3.1.tgz",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/node/test-pkg-1.3.1.tgz/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/node/1/test-pkg-1.3.1.tgz/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/node/1/test-pkg-1.3.1.tgz"
  }
]
```

<a id="resource_packages_method_python_versions"></a>

### python\_versions

List Python Package Versions

```
GET /api/v1/repos/:user_id/:repo/package/python/:package/versions.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package.

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of all the versions for this package.

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/versions.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "packagecloud-test",
    "distro_version": "python",
    "created_at": "2017-03-14T15:58:49.000Z",
    "version": "0.9.7b1",
    "release": null,
    "epoch": null,
    "private": false,
    "type": "python",
    "filename": "packagecloud_test-0.9.7b1-py2.py3-none-any.whl",
    "uploader_name": "test_user",
    "indexed": false,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1.json",
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/python/packagecloud-test/0.9.7b1/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/python/packagecloud_test-0.9.7b1-py2.py3-none-any.whl",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/python/packagecloud_test-0.9.7b1-py2.py3-none-any.whl/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/python/1/packagecloud_test-0.9.7b1-py2.py3-none-any.whl/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/python/1/packagecloud_test-0.9.7b1-py2.py3-none-any.whl"
  }
]
```

<a id="resource_packages_method_java_versions"></a>

### java\_versions

List Java Package Versions

```
GET /api/v1/repos/:user_id/:repo/package/java/maven2/:group/:package/versions.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:group` `String` The group of the package.
- `:package` `String` The name of the package.

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of all the versions for this package.

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/java/maven2/io.packagecloud/jake/versions.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "jake",
    "distro_version": "java/maven2",
    "created_at": "2017-03-13T23:54:48.000Z",
    "version": "2.3",
    "release": null,
    "epoch": null,
    "private": false,
    "type": "java",
    "filename": "jake-2.3.jar",
    "uploader_name": "test_user",
    "indexed": true,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/java/maven2/io.packagecloud/jake/2.3.json",
    "downloads_detail_url": "N/A",
    "downloads_series_url": "N/A",
    "downloads_count_url": "N/A",
    "package_html_url": "/test_user/test_repo/packages/java/jake-2.3.jar",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/java/io.packagecloud/jake-2.3.jar/artifacts/jake-2.3.jar/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/java/maven2/io.packagecloud/jake-2.3.jar/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/java/maven2/io.packagecloud/jake-2.3.jar"
  }
]
```

<a id="resource_packages_method_anyfile_versions"></a>

### anyfile\_versions

List Anyfile Package Versions

```
GET /api/v1/repos/:user_id/:repo/package/anyfile/:package/versions.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:package` `String` The name of the package.

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of all the versions for this package.

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Index API](#resource_packages_method_index)
- [Search API](#resource_packages_method_search)

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/package/anyfile/hello/versions.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "hello",
    "distro_version": "anyfile/1",
    "created_at": "2017-03-13T23:54:48.000Z",
    "version": "0.0.4",
    "release": null,
    "epoch": null,
    "private": false,
    "type": "anyfile",
    "filename": "hello-0.0.4.asc",
    "uploader_name": "test_user",
    "indexed": false,
    "sha256sum": "f101e1f32d7e4863c3e983b3709fe1755a34a8f45184ef507868267c23f76f0e",
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.4.json
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.4/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.4/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/anyfile/hello/0.0.4/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/anyfile/hello-0.0.4.asc",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/anyfile/hello-0.0.4.asc/download?distro_version_id=129",
    "promote_url": "/api/v1/repos/test_user/test_repo/anyfile/1/hello-0.0.4.asc/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/anyfile/1/hello-0.0.4.asc"
  }
]
```

<a id="resource_packages_method_index"></a>

### index

List Packages by type, distribution, version, and architecture, grouped by package version

```
GET /api/v1/repos/:user_id/:repo/packages/:type/:distro/:version/:arch.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.
- `:type` `String` The type of package it is, "rpm" or "deb".
- `:distro` `String` The name of the distribution the package is in. (i.e. ubuntu)
- `:version` `String` The version name of the distribution the package is in. (i.e. precise)

#### Query Params:

- `:arch` `String` The architecture to search for.

#### Response:

[PackageVersion](#object_PackageVersion) A JSON array of all packages that match the criteria.

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/packages/rpm.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "jake",
    "versions_count": 1,
    "versions_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/versions.json",
    "repository_url": "/api/v1/repos/test_user/test_repo",
    "repository_html_url": "/test_user/test_repo"
  }
]
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/rpm/el.json"
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/gem.json"
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/python.json"
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/node.json"
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/deb/ubuntu/precise.json"
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/deb/ubuntu/precise.json"
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/deb/ubuntu/precise/amd64.json"
```

#### Example request(s):

```
 curl "https://packagecloud.io/api/v1/repos/julio/testrepo/packages/deb/*/*/amd64.json"
```

<a id="resource_packages_method_all"></a>

### all

List All Packages (not grouped by package version)

```
GET /api/v1/repos/:user_id/:repo/packages.json
```

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of the repository.

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of PackageFragment objects.

#### Example request(s):

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/packages.json"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "jake",
    "distro_version": "fedora/22",
    "created_at": "2017-03-13T02:49:29.000Z",
    "version": "1.0",
    "release": "1.el6",
    "epoch": 0,
    "private": false,
    "type": "rpm",
    "filename": "jake-1.0-1.el6.x86_64.rpm",
    "uploader_name": "test_user",
    "indexed": false,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm"
  },
  {
    "name": "jake",
    "distro_version": "java/maven2",
    "created_at": "2017-03-13T23:54:48.000Z",
    "version": "2.3",
    "release": null,
    "epoch": null,
    "private": false,
    "type": "java",
    "filename": "jake-2.3.jar",
    "uploader_name": "test_user",
    "indexed": true,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/java/maven2/io.packagecloud/jake/2.3.json",
    "downloads_detail_url": "N/A",
    "downloads_series_url": "N/A",
    "downloads_count_url": "N/A",
    "package_html_url": "/test_user/test_repo/packages/java/jake-2.3.jar",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/java/io.packagecloud/jake-2.3.jar/artifacts/jake-2.3.jar/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/java/maven2/io.packagecloud/jake-2.3.jar/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/java/maven2/io.packagecloud/jake-2.3.jar"
  }

]
```

<a id="resource_packages_method_destroy_gem"></a>

### destroy\_gem

```
DELETE /api/v1/repos/:user_id/:repo/gems/:package.gem
```

#### URL Params:

- `:user_id` `String` The owner of the repo.
- `:repo` `String` The name of the repo.
- `:package` `String` The name of the package to be yanked.

#### Response:

`Empty` An empty JSON hash.

#### Example request(s):

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/cooluser/mystuff/gems/jake-1.0.0.gem"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{}
```

<a id="resource_packages_method_destroy_java"></a>

### destroy\_java

```
DELETE /api/v1/repos/:user_id/:repo/java/maven2/:group/:filename
```

#### URL Params:

- `:user_id` `String` The owner of the repo.
- `:repo` `String` The name of the repo.
- `:group` `String` The name of the group this package belongs to.
- `:filename` `String` The filename of the package to be yanked.

#### Response:

`Empty` An empty JSON hash.

#### Example request(s):

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/test_user/test_repo/java/maven2/io.packagecloud/jake-2.3.jar"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{}
```

<a id="resource_packages_method_destroy"></a>

### destroy

```
DELETE /api/v1/repos/:user_id/:repo/:distro/:version/:package.:ext
```

#### URL Params:

- `:user_id` `String` The owner of the repo.
- `:repo` `String` The name of the repo.
- `:distro` `String` The name of the distribution the package is in. (i.e. ubuntu)
- `:version` `String` The version name of the distribution the package is in. (i.e. precise)
- `:package` `String` The name of the package to be yanked.
- `:ext` `String` The file extension of the package to be yanked.

#### Query Params:

- `:scope` `String` The package scope. Required if deleting a scoped Node.JS package. Include the escaped '@', (i.e. ?scope=%40example).

#### Response:

`Empty` An empty JSON hash.

#### Example request(s):

##### Deleting an Ubuntu Precise package

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/cooluser/mystuff/ubuntu/precise/jake_1.0-7.dsc"
```

##### Deleting an Enterprise Linux 6.0 package:

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/cooluser/mystuff/el/6/jake-1.0-2.el6.x86_64.rpm"
```

##### Deleting a Python package:

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/cooluser/mystuff/pypi/1/packagecloud_test-0.9.7b1.zip"
```

##### Deleting a Java package:

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/cooluser/mystuff/java/maven2/jake-2.3.jar"
```

##### Deleting an unscoped Node.JS package:

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/cooluser/mystuff/node/1/packagecloud-test-1.0.0.tgz"
```

##### Deleting a scoped Node.JS package:

```
curl -X DELETE "https://packagecloud.io/api/v1/repos/cooluser/mystuff/node/1/packagecloud-test-1.0.0.tgz?scope=%40example"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{}
```

<a id="resource_packages_method_search"></a>

### search

```
GET /api/v1/repos/:user_id/:repo/search.json
```

#### Query Params:

- `:q` `String` The query string to search for package filename. If empty string is passed, all packages are returned
- `:filter` `String` Search by package type (RPMs, Debs, DSCs, Gem, Python, Node) - Ignored when [:dist] is present.
- `:dist` `String` The name of the distribution the package is in. (i.e. ubuntu, el/6) - Overrides [:filter]
- `:arch` `String` The architecture of the packages. (i.e. x86\_64, arm64, amd64) - Alpine/RPM/Debian only.
- `:per_page` `String` The number of packages to return from the results set. If nothing passed, default is 30

#### Response:

[PackageFragment](#object_PackageFragment) A JSON array of PackageFragment objects hat match the query parameters.

#### Example request(s):

###### Note:

Pass pagination information using the following headers listed here:

[API Pagination](#pagination)

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/search?q="
```

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/search?filter=rpms&per_page=1"
```

```
curl "https://packagecloud.io/api/v1/repos/test_user/test_repo/search?q=jake&dist=ubuntu&per_page=1"
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
[
  {
    "name": "jakedotrb",
    "distro_version": "RubyGem",
    "created_at": "2017-03-14T14:31:16.000Z",
    "version": "0.0.1",
    "release": null,
    "epoch": null,
    "private": false,
    "type": "gem",
    "filename": "jakedotrb-0.0.1.gem",
    "uploader_name": "test_user",
    "indexed": false,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1.json",
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/gem/jakedotrb/0.0.1/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/gems/jakedotrb-0.0.1.gem",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/gems/jakedotrb-0.0.1.gem/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem"
  },
  {
    "name": "jake",
    "distro_version": "fedora/22",
    "created_at": "2017-03-13T02:49:29.000Z",
    "version": "1.0",
    "release": "1.el6",
    "epoch": 0,
    "private": false,
    "type": "rpm",
    "filename": "jake-1.0-1.el6.x86_64.rpm",
    "uploader_name": "test_user",
    "indexed": false,
    "repository_html_url": "/test_user/test_repo",
    "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
    "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
    "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
    "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
    "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
    "download_url": "https://packagecloud.io/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm/download",
    "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
    "destroy_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm"
  }

]
```

<a id="resource_read_tokens"></a>

## read\_tokens

<a id="resource_read_tokens_method_index"></a>

### index

List read tokens for a master token.

```
GET /api/v1/repos/:user_id/:repo/master_tokens/:master_token/read_tokens.json
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:master_token` `String` The value or id of the master\_token.

#### Response:

`Array<ReadToken>` An array of read token objects that belong to this repository.

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos/username/reponame/master_tokens/123/read_tokens.json
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
   "read_tokens" : [
      {
         "id" : 1234,
         "value" : "3fe453060fd7f017219e308eb98ccf273b4c3655ba57577a",
         "name" : "app1.someservice.com"
      }
   ]
}
```

<a id="resource_read_tokens_method_create"></a>

### create

Create a read token.

```
POST /api/v1/repos/:user_id/:repo/master_tokens/:master_token/read_tokens.json
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:master_token` `String` The value or id of the master\_token.
- `read_token[name]` `String` The name of the token to create.

#### Response:

[ReadToken](#object_ReadToken) The newly created read token object.

#### Example request(s):

```
curl -X POST -F "read_token[name]=tokename" https://packagecloud.io/api/v1/repos/username/reponame/master_tokens/123/read_tokens.json
```

#### Example response:

```
< HTTP/1.1 201 Created
{"name":"tokenname","value":"ea6eef3f26bdcaa5a10ed32b5f8262dbad233900b2571a1c"}
```

<a id="resource_read_tokens_method_destroy"></a>

### destroy

Destroy a read token

```
DELETE /api/v1/repos/:user_id/:repo/master_tokens/:master_token/read_tokens/:id
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:master_token` `String` The value or id of the master\_token.
- `:id` `Integer` The id of the read token to be destroyed.

#### Example request(s):

```
curl -X DELETE https://packagecloud.io/api/v1/repos/username/reponame/master_tokens/123/read_tokens/33
```

#### Example response:

```
< HTTP/1.1 204 OK
```

<a id="resource_read_tokens_method_show"></a>

### show

View a single read token

```
GET /api/v1/repos/:user_id/:repo/master_tokens/:master_token/read_tokens/:id
```

#### URL Params:

- `:user_id` `String` The username to which the repo belongs.
- `:repo` `String` The name of the repo.
- `:master_token` `String` The value or id of the master\_token.
- `:id` `Integer` The id of the read token to view

#### Example request(s):

```
curl -X GET https://packagecloud.io/api/v1/repos/username/reponame/master_tokens/123/read_tokens/33
```

#### Example response:

```
< HTTP/1.1 200 OK
```

```
{
   "id" : 1234,
   "value" : "3fe453060fd7f017219e308eb98ccf273b4c3655ba57577a",
   "name" : "app1.someservice.com"
}
```

<a id="resource_repositories"></a>

## repositories

<a id="resource_repositories_method_index"></a>

### index

```
GET /api/v1/repos
```

#### Query Params:

- `include_collaborations` `String` Include to return Repository objects from
  collaborations in addition to objects that belong to your account.

#### Response:

`Array<Repository>` An array of Repository objects that belong to your account.

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos
```

#### Example response:

```
[{
   "name": "myrepo",
   "created_at": "2014-02-26T00:03:28.000Z",
   "url": "https://packagecloud.io/cooluser/myrepo",
   "last_push_human": "3 days ago",
   "package_count_human": "17 packages",
   "private": false,
   "fqname": "cooluser/myrepo"
 },
 {
   "name": "myrepo2",
   "created_at": "2014-03-25T19:16:26.000Z",
   "url": "https://packagecloud.io/cooluser/myrepo2",
   "last_push_human": "6 days ago",
   "package_count_human": "3 packages",
   "private": false,
   "fqname": "cooluser/myrepo2"
}]
```

<a id="resource_repositories_method_create"></a>

### create

```
POST /api/v1/repos
```

#### URL Params:

- `name` `String` The repository name.
- `private` `Boolean` Whether the repo to be created is private.

#### Response:

`String` The URL of the new repository resource.

#### Example request(s):

```
curl -X POST                                                  \
     -H "Content-Type: application/json"                      \
     -d '{"repository": {"name": "thename", "private": "1"}}' \
     "https://packagecloud.io/api/v1/repos.json"
```

#### Example response:

```
{"url": "https://packagecloud.io/cooluser/thename"}
```

<a id="resource_repositories_method_show"></a>

### show

```
GET /api/v1/repos/:user_id/:name
```

#### URL Params:

- `:user_id` `String` The username of the owner.
- `:name` `String` The name of the repo.

#### Response:

[Repository](#object_Repository) The repository object

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos/cooluser/myrepo
```

#### Example response:

```
{
  "name": "myrepo",
  "created_at": "2014-02-26T00:03:28.000Z",
  "url": "https://packagecloud.io/cooluser/myrepo",
  "last_push_human": "3 days ago",
  "package_count_human": "17 packages",
  "private": false,
  "fqname": "cooluser/myrepo"
}
```

<a id="resource_repositories_method_packages_with_bk_required_attributes"></a>

### packages\_with\_bk\_required\_attributes

```
GET /api/v1/repos/:user_id/:repo/packages_with_bk_required_attributes
```

#### URL Params:

- `repository_uuid` `String` The UUID of the repository

#### Query Params:

- `anyfile_attr_fix` `Boolean` True/False

#### Response:

`Array` Array of packages with storage usage, blob, and ecosystem-specific attributes

#### Example request(s):

```
curl https://packagecloud.io/api/v1/repos/cooluser/myrepo/packages_with_bk_required_attributes
```

#### Example response:

```
{
  "packages": [
    "package": {
      "id": 6,
      "created_at": "2025-10-22T07:49:39.000Z",
      "updated_at": "2025-10-22T07:50:08.000Z",
      "deleted_at": "2025-10-22T07:50:08.000Z",
      "deleted_by_id": 2,
      "filename": "bye-2.0.1.zip",
      "family": "bye",
      "release": "2.0.1",
      "variant": "zip",
      "distro_version_id": 1,
      "metadata": {
        "semver": {
          "major": "2",
          "minor": "0",
          "patch": "1",
          "prerelease": null,
          "buildmetadata": null
        }
      },
      "weekly_downloads": {},
      "digest": "ea87009e7e679bec8c57798aaca7b5341ec639e15c57b5da1d51d41cff3a8093",
      "bucket_name": "packagecloud-repositories-development",
      "bucket_storage_path": "2/134/anyfile/packages/6.zip",
      "target_bucket_storage_path": "018ca431-b028-7565-b846-e806ef4b72af/019a0add-2b10-70ff-b727-f490aba5cbb6/blobs/<BLOB_UUID>/bye-2.0.1.zip"
    }
  ]
}
```

<a id="resource_stats"></a>

## stats

<a id="resource_stats_method_downloads_count"></a>

### downloads\_count

Retrieve the number of times a particular package has been downloaded given a
particular criteria. This is specific to a single package inside a repository.

###### Note:

Default date range is 7 days ago.

##### debian/redhat

```
GET /api/v1/repos/:user_id/:repo/package/:type/:distro/:version/:package/:arch/:package_version/:release/stats/downloads/count.json
```

##### gem

```
GET /api/v1/repos/:user_id/:repo/package/gem/:package/:version/stats/downloads/count.json
```

##### python

```
GET /api/v1/repos/:user_id/:repo/package/python/:package/:version/stats/downloads/count.json
```

##### node.js

```
GET /api/v1/repos/:user_id/:repo/package/node/:package/:version/stats/downloads/count.json
```

#### Permissions:

Everyone for public repositories, Owners & Collaborators for private repositories.

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of this repository.
- `:package` `String` The name of the package. If the package is a scoped Node.JS package include the scope and an escaped '/' (e.g. @scope%2Fname).

#### Query Params:

- `:start_date` `String` The ISO8601 starting date (e.g., 20160231Z).
- `:end_date` `String` The ISO8601 ending date (e.g., 20160231Z).
- `:master_token` `String` The master\_token name or id to filter downloads by.
- `:read_token` `String` The read\_token name or id to filter downloads by (:master\_token required).
- `:user_agent` `String` The user\_agent to filter downloads by.
- `:source` `String` The source to filter downloads by, must be "web" or "cli"

#### Response:

[CountValue](#object_CountValue) JSON object containing the value of the result.

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Python Versions API](#resource_packages_method_python_versions)
- [RubyGem Versions API](#resource_packages_method_gem_versions)
- [Node.js Versions API](#resource_packages_method_node_versions)
- [Index API](#resource_packages_method_index)

##### Gem Downloads Count for `my-gem-1.2.0.gem`:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/count.json
```

##### Python Downloads Count for `packagecloud_test-1.2.1-py2.7.egg`:

```
/api/v1/repos/julio/test_repo/package/python/packagecloud-test/1.2.1/stats/downloads/count.json
```

##### RPM Downloads Count for `jake-1.0-2.x86_64.rpm` on Fedora 18:

```
/api/v1/repos/julio/test_repo/package/rpm/fedora/18/jake/x86_64/1.0/2/stats/downloads/count.json
```

##### Debian Downloads Count for `jake1.0-7amd64.deb` on Ubuntu Hardy:

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/count.json
```

##### Debian Downloads Count for `jake1.0-7amd64.deb` on Ubuntu Hardy for User Agent "MyClient1":

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/count.json?user_agent=MyClient1
```

##### Debian Downloads Count for `jake1.0-7amd64.deb` on Ubuntu Hardy and Read Token "database":

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/count.json?read_token=database
```

##### Gem Downloads Count for `my-gem-1.2.0.gem` for all time:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/count.json?start_date=19700101Z
```

##### Gem Downloads Count for `my-gem-1.2.0.gem` for all time CLI downloads:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/count.json?start_date=19700101Z&source=cli
```

##### Node.js Downloads Count for `test-pkg-1.3.1.tgz` for all time:

```
/api/v1/repos/julio/test_repo/package/node/test-pkg/1.3.1/stats/downloads/count.json?start_date=19700101Z&source=cli
```

##### Node.js Downloads Count for scoped package `@scope/test-pkg-1.3.1.tgz` for all time:

```
/api/v1/repos/julio/test_repo/package/node/@scope%2Ftest-pkg/1.3.1/stats/downloads/count.json?start_date=19700101Z&source=cli
```

#### Example response:

```
< HTTP/1.0 200 OK
```

```
{
  "value": 5135
}
```

<a id="resource_stats_method_downloads_detail"></a>

### downloads\_detail

Retrieve the details of all the downloads for a particular package given a
particular criteria. This is specific to a single package inside a repository.

###### Note:

Default date range is 7 days ago. See response headers for [pagination](#pagination) information.

##### debian/redhat

```
GET /api/v1/repos/:user_id/:repo/package/:type/:distro/:version/:package/:arch/:package_version/:release/stats/downloads/detail.json
```

##### gem

```
GET /api/v1/repos/:user_id/:repo/package/gem/:package/:version/stats/downloads/detail.json
```

##### python

```
GET /api/v1/repos/:user_id/:repo/package/python/:package/:version/stats/downloads/detail.json
```

##### node.js

```
GET /api/v1/repos/:user_id/:repo/package/node/:package/:version/stats/downloads/detail.json
```

#### Permissions:

Repository owners only

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of this repository.
- `:package` `String` The name of the package. If the package is a scoped Node.JS package include the scope and an escaped '/' (e.g. @scope%2Fname).
- `:version` `String` The version number of the package.

#### Query Params:

- `:start_date` `String` An ISO8601 starting date (e.g., 20160231Z).
- `:end_date` `String` An ISO8601 ending date (e.g., 20160231Z).
- `:master_token` `String` The master\_token name or id to filter downloads by.
- `:read_token` `String` The read\_token name or id to filter downloads by (:master\_token required).
- `:user_agent` `String` The user\_agent to filter downloads by.
- `:source` `String` The source to filter downloads by, must be "web" or "cli."

#### Response:

[PackageDownloads](#object_PackageDownloads) JSON object containing details of all downloads

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Python Versions API](#resource_packages_method_python_versions)
- [RubyGem Versions API](#resource_packages_method_gem_versions)
- [Node.js Versions API](#resource_packages_method_node_versions)
- [Index API](#resource_packages_method_index)

##### Gem Downloads Details for `my-gem-1.2.0.gem`:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/detail.json
```

##### Python Downloads Details for `packagecloud_test-1.2.1-py2.7.egg`:

```
/api/v1/repos/julio/test_repo/package/python/packagecloud-test/1.2.1/stats/downloads/detail.json
```

##### RPM Downloads Details for `jake-1.0-2.x86_64.rpm` on Fedora 18:

```
/api/v1/repos/julio/test_repo/package/rpm/fedora/18/jake/x86_64/1.0/2/stats/downloads/detail.json
```

##### Debian Downloads Details for `jake1.0-7amd64.deb` on Ubuntu Hardy:

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/detail.json
```

##### Debian Downloads Details for `jake1.0-7amd64.deb` on Ubuntu Hardy for User Agent "MyClient1":

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/detail.json?user_agent=MyClient1
```

##### Debian Downloads Details for `jake1.0-7amd64.deb` on Ubuntu Hardy and Read Token "database":

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/detail.json?read_token=database
```

##### Gem Downloads Details for `my-gem-1.2.0.gem` for all time:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/detail.json?start_date=19700101Z
```

##### Gem Downloads Details for `my-gem-1.2.0.gem` for all time CLI downloads:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/detail.json?start_date=19700101Z&source=cli
```

##### Node.js Downloads Details for `test-pkg-1.3.1.tgz` for all time:

```
/api/v1/repos/julio/test_repo/package/node/test-pkg/1.3.1/stats/downloads/detail.json?start_date=19700101Z
```

##### Node.js Downloads Details for scoped package `@scope/test-pkg-1.3.1.tgz` for all time:

```
/api/v1/repos/julio/test_repo/package/node/@scope%2Ftest-pkg/1.3.1/stats/downloads/detail.json?start_date=19700101Z
```

#### Example response:

```
< HTTP/1.0 200 OK
```

```
{
  "downloaded_at": 2015-04-12T05:36:53.000Z,
  "ip_address": "12.51.22.21",
  "user_agent": "Ruby",
  "source": "cli",
  "read_token": "ubuntu-51.2.aws.com"
}
```

<a id="resource_stats_method_downloads_series"></a>

### downloads\_series

Retrieve a time series of all the downloads for a particular package given a
particular criteria. This is specific to a single package inside a repository.

###### Note:

Default date range is 7 days ago. See response headers for [pagination](#pagination) information.

##### debian/redhat

```
GET /api/v1/repos/:user_id/:repo/package/:type/:distro/:version/:package/:arch/:package_version/:release/stats/downloads/series/:interval.json
```

##### gem

```
GET /api/v1/repos/:user_id/:repo/package/gem/:package/:version/stats/downloads/series/:interval.json
```

##### python

```
GET /api/v1/repos/:user_id/:repo/package/python/:package/:version/stats/downloads/series/:interval.json
```

##### node.js

```
GET /api/v1/repos/:user_id/:repo/package/node/:package/:version/stats/downloads/series/:interval.json
```

#### Permissions:

Everyone for public repositories, Owners & Collaborators for private repositories.

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of this repository.
- `:package` `String` The name of the package. If the package is a scoped Node.JS package include the scope and an escaped '/' (e.g. @scope%2Fname).
- `:version` `String` The version number of the package.

#### Query Params:

- `:start_date` `String` An ISO8601 starting date (e.g., 20160231Z).
- `:end_date` `String` An ISO8601 end date (e.g., 20160231Z).
- `:master_token` `String` The master\_token name or id to filter downloads by.
- `:read_token` `String` The read\_token name or id to filter downloads by (:master\_token required).
- `:user_agent` `String` The user\_agent to filter downloads by.
- `:source` `String` The source to filter downloads by, must be "web" or "cli"

#### Response:

[SeriesValue](#object_SeriesValue) JSON object containing details of all downloads

#### Example request(s):

###### Note:

Instead of constructing these URLs by hand, you should use the generated versions
returned from any of these API's, which are guaranteed to be correct for all supported package types:

- [All API](#resource_packages_method_all)
- [Versions API](#resource_packages_method_versions)
- [Python Versions API](#resource_packages_method_python_versions)
- [RubyGem Versions API](#resource_packages_method_gem_versions)
- [Node.js Versions API](#resource_packages_method_node_versions)
- [Index API](#resource_packages_method_index)

##### Gem Downloads Series for `my-gem-1.2.0.gem`:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/series/daily.json
```

##### Python Downloads Series for `packagecloud_test-1.2.1-py2.7.egg`:

```
/api/v1/repos/julio/test_repo/package/python/packagecloud-test/1.2.1/stats/downloads/series/daily.json
```

##### RPM Downloads Series for `jake-1.0-2.x86_64.rpm` on Fedora 18:

```
/api/v1/repos/julio/test_repo/package/rpm/fedora/18/jake/x86_64/1.0/2/stats/downloads/series/daily.json
```

##### Debian Downloads Series for `jake1.0-7amd64.deb` on Ubuntu Hardy:

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/series/daily.json
```

##### Debian Downloads Series for `jake1.0-7amd64.deb` on Ubuntu Hardy for User Agent "MyClient1":

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/series/daily.json?user_agent=MyClient1
```

##### Debian Downloads Series for `jake1.0-7amd64.deb` on Ubuntu Hardy and Read Token "database":

```
/api/v1/repos/julio/test_repo/package/deb/ubuntu/hardy/jake/amd64/1.0-7/stats/downloads/series/daily.json?read_token=database
```

##### Gem Downloads Series for `my-gem-1.2.0.gem` for all time:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/series/daily.json?start_date=19700101Z
```

##### Gem Downloads Series for `my-gem-1.2.0.gem` for all time CLI downloads:

```
/api/v1/repos/julio/test_repo/package/gem/my-gem/1.2.0/stats/downloads/series/daily.json?start_date=19700101Z&source=cli
```

##### Node.js Downloads Series for `test-pkg-1.3.1.tgz` for all time:

```
/api/v1/repos/julio/test_repo/package/node/test-pkg/1.3.1/stats/downloads/series/daily.json?start_date=19700101Z
```

##### Node.js Downloads Series for scoped package `@scope/test-pkg-1.3.1.tgz` for all time:

```
/api/v1/repos/julio/test_repo/package/node/@scope%2Ftest-pkg/1.3.1/stats/downloads/series/daily.json?start_date=19700101Z
```

#### Example response:

```
< HTTP/1.0 200 OK
```

```
{
 "20160221Z": 22,
 "20160222Z": 21,
 "20160223Z": 29,
 "20160224Z": 19,
 "20160225Z": 30,
 "20160226Z": 38,
 "20160227Z": 40
}
```

<a id="resource_stats_method_installs_count"></a>

### installs\_count

Retrieve the number of times a particular repository has been installed given a
particular criteria. This is specific to a single repository.

###### Note:

Default date range is 7 days ago.

##### all

```
GET /api/v1/repos/:user_id/:repo/stats/installs/count.json
```

##### by distro

```
GET /api/v1/repos/:user_id/:repo/stats/installs/:distro/count.json
```

##### by distro and version

```
GET /api/v1/repos/:user_id/:repo/stats/installs/:distro/:version/count.json
```

#### Permissions:

Everyone for public repositories, Owners & Collaborators for private repositories.

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of this repository.
- `:distro` `String` The name of the distribution to filter repository installs by (i.e. ubuntu)
- `:version` `String` The version name of the distribution to filter repository installs by (i.e. precise)

#### Query Params:

- `:start_date` `String` ISO8601 starting date, like 20160231Z.
- `:end_date` `String` ISO8601 ending date, like 20160231Z.
- `:master_token` `String` The master\_token name or id to filter repository installs by.
- `:user_agent` `String` The user\_agent to filter repository installs by.

#### Response:

[CountValue](#object_CountValue) JSON object containing the value of the result.

#### Example request(s):

##### Repository Installs Count for `testuser/testrepo` across all operating systems and distributions:

```
/api/v1/repos/julio/test_repo/stats/installs/count.json
```

##### Repository Installs Count for `testuser/testrepo` across all Ubuntu distributions:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/count.json
```

##### Repository Installs Count for `testuser/testrepo` specifically for Ubuntu Precise Pangolin:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/precise/count.json
```

##### Repository Installs Count for `testuser/testrepo` specifically for Ubuntu Precise Pangolin for all time:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/precise/count.json?start_date=19700101Z
```

##### Repository Installs Count for `testuser/testrepo` across all Ubuntu distributions matching a specific token:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/count.json?master_token=datacenter-2
```

#### Example response:

```
< HTTP/1.0 200 OK
```

```
{
  "value": 5135
}
```

<a id="resource_stats_method_installs_detail"></a>

### installs\_detail

Retrieve the details of all repository installations that match a
particular criteria. This is specific to a single repository.

###### Note:

Default date range is 7 days ago. See response headers for [pagination](#pagination) information.

##### all

```
GET /api/v1/repos/:user_id/:repo/stats/installs/detail.json
```

##### by distro

```
GET /api/v1/repos/:user_id/:repo/stats/installs/:distro/detail.json
```

##### by distro and version

```
GET /api/v1/repos/:user_id/:repo/stats/installs/:distro/:version/detail.json
```

#### Permissions:

Repository owners only

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of this repository.
- `:distro` `String` The name of the distribution to filter repository installs by (i.e. ubuntu)
- `:version` `String` The version name of the distribution to filter repository installs by (i.e. precise)

#### Query Params:

- `:start_date` `String` ISO8601 starting date, like 20160231Z.
- `:end_date` `String` ISO8601 ending date, like 20160231Z.
- `:master_token` `String` The master\_token name or id to filter repository installs by.
- `:user_agent` `String` The user\_agent to filter repository installs by.

#### Response:

[RepositoryInstalls](#object_RepositoryInstalls) JSON object containing the details of repository installs.

#### Example request(s):

##### Repository Installs Details for `testuser/testrepo` across all operating systems and distributions:

```
/api/v1/repos/julio/test_repo/stats/installs/detail.json
```

##### Repository Installs Details for `testuser/testrepo` across all Ubuntu distributions:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/detail.json
```

##### Repository Installs Details for `testuser/testrepo` specifically for Ubuntu Precise Pangolin:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/precise/detail.json
```

##### Repository Installs Details for `testuser/testrepo` specifically for Ubuntu Precise Pangolin for all time:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/precise/detail.json?start_date=19700101Z
```

##### Repository Installs Details for `testuser/testrepo` across all Ubuntu distributions matching a specific token:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/detail.json?master_token=datacenter-2
```

#### Example response:

```
< HTTP/1.0 200 OK
```

```
{
  "installed_at": 2015-04-12T05:36:53.000Z,
  "ip_address": "12.51.22.21",
  "hostname": "localhost.localdomain",
  "user_agent": "Ruby",
  "master_token": "default",
  "distro_version": "ubuntu/precise"
}
```

<a id="resource_stats_method_installs_series"></a>

### installs\_series

Retrieve a time series of all the repository installs that match a
particular criteria for a give time period. This is specific to a single repository.

###### Note:

Default date range is 7 days ago. See response headers for [pagination](#pagination) information.

##### all

```
GET /api/v1/repos/:user_id/:repo/stats/installs/series/:interval.json
```

##### by distro

```
GET /api/v1/repos/:user_id/:repo/stats/installs/:distro/series/:interval.json
```

##### by distro and version

```
GET /api/v1/repos/:user_id/:repo/stats/installs/:distro/:version/series/:interval.json
```

#### Permissions:

Everyone for public repositories, Owners & Collaborators for private repositories.

#### URL Params:

- `:user_id` `String` The user this repo belongs to.
- `:repo` `String` The name of this repository.
- `:distro` `String` The name of the distribution to filter repository installs by (i.e. ubuntu)
- `:version` `String` The version name of the distribution to filter repository installs by (i.e. precise)
- `:interval` `String` The version name of the distribution to filter repository installs by (i.e. precise)

#### Query Params:

- `:start_date` `String` ISO8601 starting date, like 20160231Z.
- `:end_date` `String` ISO8601 ending date, like 20160231Z.
- `:master_token` `String` The master\_token name or id to filter repository installs by.
- `:user_agent` `String` The user\_agent to filter repository installs by.

#### Response:

[RepositoryInstalls](#object_RepositoryInstalls) JSON object containing the details of repository installs.

#### Example request(s):

##### Repository Installs Series for `testuser/testrepo` across all operating systems and distributions:

```
/api/v1/repos/julio/test_repo/stats/installs/series/weekly.json
```

##### Repository Installs Series for `testuser/testrepo` across all Ubuntu distributions:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/series/weekly.json
```

##### Repository Installs Series for `testuser/testrepo` specifically for Ubuntu Precise Pangolin:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/precise/series/weekly.json
```

##### Repository Installs Series for `testuser/testrepo` specifically for Ubuntu Precise Pangolin for all time:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/precise/series/weekly.json?start_date=19700101Z
```

##### Repository Installs Series for `testuser/testrepo` across all Ubuntu distributions matching a specific token:

```
/api/v1/repos/julio/test_repo/stats/installs/ubuntu/series/weekly.json?master_token=datacenter-2
```

#### Example response:

```
< HTTP/1.0 200 OK
```

```
{
 "20160221Z": 22,
 "20160222Z": 21,
 "20160223Z": 29,
 "20160224Z": 19,
 "20160225Z": 30,
 "20160226Z": 38,
 "20160227Z": 40
}
```

<a id="object_CountValue"></a>

## CountValue

#### Fields:

- `value` The value of the result

#### Example:

```
{
   "value": 12312
}
```

#### See Also:

The [docs](#resource_stats_method_downloads_count) Package Downloads count API

The [docs](#resource_stats_method_installs_count) Repository Installs count API

<a id="object_GPGKey"></a>

## GPGKey

#### Fields:

- `name` The name of the GPG key.
- `fingerprint` The GPG key's fingerprint.
- `keytype` The GPG key type ('repo' for repository signing keys or 'package' for package signing keys).
- `self` The URL for this object.
- `destroy_url` The URL that can be used to delete this GPG key.
- `download_url` The URL that can be used to download the GPG public key data.

#### Example:

```
{
  "name" : "user-repo-99A35B3F55E8EB3B.pub.gpg",
  "fingerprint" : "99A35B3F55E8EB3B",
  "keytype": "repo",
  "self": "/api/v1/repos/user/repo/gpg_keys/user-repo-99A35B3F55E8EB3B.pub.gpg.json",
  "destroy_url" : "/api/v1/repos/user/repo/gpg_keys/user-repo-99A35B3F55E8EB3B.pub.gpg.json",
  "download_url": "https://packagecloud.io/user/repo/gpgkey"
}
```

#### See Also:

The [docs](/docs#gpg) on GPG keys.

<a id="object_MasterToken"></a>

## MasterToken

#### Fields:

- `name` The name of the master token.
- `value` The value of the master token, for use in the read token API.
- `paths[self]` A URI for this master token. Can be used to destroy one.
- `read_tokens` An array of {ReadToken} objects that belong to this master token.

#### Example:

```
{
   "value" : "e5480f5b38f1f78de2aaa0fa732d1427b1b83113371fd97d",
   "name" : "default",
   "read_tokens" : [
      {
         "value" : "3fe453060fd7f017219e308eb98ccf273b4c3655ba57577a",
         "name" : "app1.somewhere.com"
      }
   ],
   "paths" : {
      "self" : "/api/v1/repos/somewhere/production/master_tokens/1"
   }
}
```

#### See Also:

The [docs](/docs#master_tokens) on master tokens.

<a id="object_MasterTokenReadTokens"></a>

## MasterTokenReadTokens

#### Fields:

- `name` The name of the master token.
- `value` The value of the master token, for use in the read token API.
- `paths[self]` A URI for this master tokens read tokens.
- `read_tokens_url` a URI to get all of the read tokens for this master token.

#### Example:

```
{
   "name" : "default",
   "value" : "e5480f5b38f1f78de2aaa0fa732d1427b1b83113371fd97d",
   "paths" : {
      "self" : "/api/v1/repos/somewhere/production/master_tokens/1"
   },
   "read_tokens_url" : "/api/v1/repos/somewhere/production/master_tokens/1/read_tokens"
}
```

#### See Also:

The [docs](/docs#master_tokens) on master tokens.

<a id="object_MasterTokensResult"></a>

## MasterTokensResult

#### Fields:

- `name` The name of the master token.
- `value` The value of the master token, for use in the read token API.
- `self_url` A URI for this master token. Can be used to destroy one.
- `read_tokens_url` a URI to get all of the read tokens for this master token.

#### Example:

```
{
   "name" : "default",
   "value" : "e5480f5b38f1f78de2aaa0fa732d1427b1b83113371fd97d",
   "self_url" : "/api/v1/repos/somewhere/production/master_tokens/1",
   "read_tokens_url" : "/api/v1/repos/somewhere/production/master_tokens/1"
}
```

#### See Also:

The [docs](/docs#master_tokens) on master tokens.

<a id="object_PackageDetails"></a>

## PackageDetails

```
{
  "name": "jake",
  "distro_version": "fedora/22",
  "architecture": "x86_64",
  "repository": "test_repo",
  "size": "3712",
  "summary": "jake douglas is a very nice young man.",
  "filename": "jake-1.0-1.el6.x86_64.rpm",
  "description": "as it so happens, jake douglas is a very nice young man.",
  "dependencies": [
    {
      "context": "requires",
      "dependencies": [
        "libc.so.6(GLIBC_2.2.5)(64bit)",
        "rtld(GNU_HASH)"
      ]
    }
  ],
  "md5sum": "5abe922fc4bbf5bbdac9b85173371892",
  "sha1sum": "062fd41ecf96587309ec9a3ae2035cc44c348b8f",
  "sha256sum": "070da5370a96ba3ae679e7d02d7de6309e4d159340d9f3b555d6d5b4b7cf260a",
  "sha512sum": "406fa288d5dfff194ec2b119b798c4658375a5d07b34f2d6350885cdf6b620f3fdeee45427fef8bcd37e6624049fba0c633b5b4030b79bf96028db6b4f01de87",
  "private": false,
  "uploader_name": "test_user",
  "created_at": "2017-03-13T02:49:29.000Z",
  "licenses": [
    "GPL"
  ],
  "version": "1.0",
  "release": "1.el6",
  "epoch": 0,
  "indexed": false,
  "scope": null,
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
  "versions_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/versions.json",
  "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
  "total_downloads_count": 0,
  "download_url": "https://packagecloud.io/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm/download",
  "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
  "destroy_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "self_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json"
}
```

#### Fields:

- `name` The name of the package.
- `distro_version` The distro\_version for the package.
- `architecture` The architecture of the package.
- `repository` The name of the repository for the package.
- `size` The size (in bytes) of the package. Returned as a String for JavaScript support.
- `summary` The summary of the package (if available).
- `filename` The filename of the package.
- `description` The description of the package (if available).
- `md5sum` The MD5 checksum for the package (if available).
- `sha1sum` The SHA1 checksum for the package (if available).
- `sha256sum` The SHA256 checksum for the package (if available).
- `sha512sum` The SHA512 checksum for the package (if available).
- `private` Whether or not the package is in a private repository.
- `uploader_name` The name of the uploader for the package.
- `created_at` When the package was uploaded.
- `licenses` Array of licenses for this package (if available).
- `version` The version of the package.
- `release` The release of the package (if available).
- `epoch` The epoch of the package (if available).
- `indexed` Whether or not this package has been indexed.
- `scope` The scope of the package (if available).
- `repository_html_url` The HTML url of the repository.
- `versions_url` The API url of other versions of this package.
- `promote_url` The API url that can be used to promote this package.
- `total_downloads_count` The number of times this package has been downloaded.
- `download_url` The url to download this package.
- `package_html_url` The HTML url for this package.
- `downloads_detail_url` The url to get access log details for package downloads.
- `downloads_series_url` The url to get time series data for package downloads.
- `downloads_count_url` The url to get the total number of package downloads.
- `destroy_url` The url for the HTTP DELETE request to destroy this package.
- `self_url` The API url for this response.

#### Example:

#### See Also:

The [docs](#resource_packages_method_show) on the Package show API.

The [docs](#resource_packages_method_gem_show) on the Rubygem show API.

<a id="object_PackageDownloads"></a>

## PackageDownloads

#### Fields:

- `downloaded_at` The date this package was downloaded (UTC)
- `ip_address` The ip address of this package download
- `user_agent` The user agent of the client which downloaded the package
- `source` The source of the package download ("web" or "cli")
- `read_token` The name of the read token (for private repositories)

#### Example:

```
{
   "downloaded_at": 2015-04-12T05:36:53.000Z,
   "ip_address": "12.51.22.21",
   "user_agent": "Ruby",
   "source": "cli",
   "read_token": "ubuntu-51.2.aws.com"
}
```

#### See Also:

The [docs](#resource_stats_method_downloads_detail) on the Package Download details API.

<a id="object_PackageFragment"></a>

## PackageFragment

#### Fields:

- `name` The name of the package.
- `created_at` When the package was uploaded.
- `distro_version` The distro\_version for the package.
- `version` The version of the package.
- `release` The release of the package (if available).
- `architecture` The architecture of the package (if available).
- `epoch` The epoch of the package (if available).
- `scope` The scope of the package (if available).
- `private` Whether or not the package is in a private repository.
- `type` The type of package ("deb", "gem", or "rpm").
- `filename` The filename of the package.
- `uploader_name` The name of the uploader for the package.
- `indexed` Whether or not this package has been indexed.
- `repository_html_url` The HTML url of the repository.
- `package_url` The API url for this package.
- `package_html_url` The HTML url for this package.
- `downloads_detail_url` The url to get access log details for package downloads.
- `downloads_series_url` The url to get time series data for package downloads.
- `downloads_count_url` The url to get the total number of package downloads.
- `promote_url` The url for promoting this to another repository.
- `destroy_url` The url for the HTTP DELETE request to destroy this package.

#### Example:

```
{
  "name": "jake",
  "distro_version": "fedora/22",
  "created_at": "2017-03-13T02:49:29.000Z",
  "version": "1.0",
  "release": "1.el6",
  "epoch": 0,
  "scope": null,
  "private": false,
  "type": "rpm",
  "filename": "jake-1.0-1.el6.x86_64.rpm",
  "uploader_name": "test_user",
  "indexed": false,
  "repository_html_url": "/test_user/test_repo",
  "package_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6.json",
  "downloads_detail_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/detail.json",
  "downloads_series_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/series/daily.json",
  "downloads_count_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/1.0/1.el6/stats/downloads/count.json",
  "package_html_url": "/test_user/test_repo/packages/fedora/22/jake-1.0-1.el6.x86_64.rpm",
  "promote_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm/promote.json",
  "delete_url": "/api/v1/repos/test_user/test_repo/fedora/22/jake-1.0-1.el6.x86_64.rpm"
}
```

#### See Also:

The [docs](#resource_packages_method_all) on the Packages List All API.

The [docs](#resource_packages_method_index) on the Package List/Filter API.

<a id="object_PackageVersion"></a>

## PackageVersion

#### Fields:

- `name` The name of the package.
- `versions_count` How many versions this package has.
- `versions_url` The API url of all versions of this package.
- `repository_url` The API url of the repository.
- `repository_html_url` The HTML url of the repository.

#### Example:

```
{
  "name": "jake",
  "versions_count": 1,
  "versions_url": "/api/v1/repos/test_user/test_repo/package/rpm/fedora/22/jake/x86_64/versions.json",
  "repository_url": "/api/v1/repos/test_user/test_repo",
  "repository_html_url": "/test_user/test_repo"
}
```

#### See Also:

The [docs](#resource_packages_method_versions) on the Packages Versions API.

The [docs](#resource_packages_method_gem_versions) on the RubyGem Versions API.

<a id="object_ReadToken"></a>

## ReadToken

#### Fields:

- `name` The name of the token. Probably the FQDN of the node that owns it.
- `value` The value of the token. This is the value to use in the actual connection string to the repo.

#### Example:

```
{
  "id"   : 231,
  "value" : "3fe453060fd7f017219e308eb98ccf273b4c3655ba57577a",
  "name" : "app1.someservice.com"
}
```

#### See Also:

The [docs](/docs#read_tokens) on read tokens.

<a id="object_Repository"></a>

## Repository

#### Fields:

- `name` The name of the repo.
- `created_at` A timestamp of when the repo was created.
- `url` The packagecloud URL for the repo.
- `last_push_human` A human readable string describing the number of packages in the repo.
- `private` A boolean value indicating whether or not the repo is private.
- `total_installs_count` The number of times this repository has been installed.
- `fqname` A string value of the fully qualified name (owner/reponame) for this repo. i.e. computology/public

#### Example:

```
{
    "name": "myrepo",
    "created_at": "2014-02-26T00:03:28.000Z",
    "url": "https://packagecloud.io/cooluser/myrepo",
    "last_push_human": "3 days ago",
    "package_count_human": "17 packages",
    "private": false,
    "total_installs_count": 1231,
    "fqname": "cooluser/myrepo"
}
```

#### See Also:

The [docs](/docs#repos) on repos.

<a id="object_RepositoryInstalls"></a>

## RepositoryInstalls

#### Fields:

- `installed_at` The date this repository was installed (UTC)
- `ip_address` The ip address of this repository install
- `user_agent` The user agent of the client which installed this repository
- `master_token` The master token associated with this repository install
- `distro_version` The distribution version this repository was installed for

#### Example:

```
{
   "installed_at": 2015-04-12T05:36:53.000Z,
   "ip_address": "12.51.22.21",
   "hostname": "localhost.localdomain",
   "user_agent": "Ruby",
   "master_token": "default",
   "distro_version": "ubuntu/precise"
}
```

#### See Also:

The [docs](#resource_stats_method_installs_detail) on the Repository Installs details API.

<a id="object_SeriesValue"></a>

## SeriesValue

#### Fields:

- A JSON hash of Dates and values

#### Example:

```
{
   "20160221Z": 22,
   "20160222Z": 21,
   "20160223Z": 29,
   "20160224Z": 19,
   "20160225Z": 30,
   "20160226Z": 38,
   "20160227Z": 40
}
```

#### See Also:

The [docs](#resource_stats_method_downloads_series) Package Downloads series API

The [docs](#resource_stats_method_installs_series) Repository Installs series API

<a id="object_APIToken"></a>

## APIToken

#### Fields:

- `token` Your packagecloud API token, used for HTTP basic authentication on subsequent requests.

#### Example:

```
{"token":"f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0"}
```

#### See Also:

The [docs](#api_tokens) on API tokens.

<a id="object_License"></a>

## License

#### Fields:

- `license` The packagecloud:enterprise license data (YAML-encoded string).
- `signature` The GPG signature of the license data, verifiable against the packagecloud GPG key.

#### Example:

```
{
  "license": "---\n:company_name: company-2\n:company_domain: www.domain2.com\n",
  "signature": "-----BEGIN PGP SIGNATURE-----\n...\n-----END PGP SIGNATURE-----\n"
}
```

#### See Also:

The [docs](#resource_licenses_method_index) on the licenses API.

<a id="object_DistroVersion"></a>

## DistroVersion

#### Fields:

- `id` The numeric id of this version. Used as the `distro_version_id` value on package-upload requests.
- `display_name` Human-readable name for the version (e.g. "5.10 Breezy Badger").
- `index_name` Short canonical name used in repository paths (e.g. "breezy").
- `version_number` The version number portion when applicable (e.g. "5.10").

#### Example:

```
{
  "id": 4,
  "display_name": "5.10 Breezy Badger",
  "index_name": "breezy",
  "version_number": "5.10"
}
```

<a id="object_Distribution"></a>

## Distribution

#### Fields:

- `display_name` Human-readable name for the distribution (e.g. "Ubuntu").
- `index_name` Short canonical name used in repository paths (e.g. "ubuntu").
- `versions` Array<DistroVersion> The known versions of this distribution.

#### Example:

```
{
  "display_name": "Ubuntu",
  "index_name": "ubuntu",
  "versions": [
    {
      "id": 4,
      "display_name": "5.10 Breezy Badger",
      "index_name": "breezy",
      "version_number": "5.10"
    }
  ]
}
```

#### See Also:

The [docs](#resource_distributions) on the distributions API.

<a id="object_PackageContents"></a>

## PackageContents

#### Fields:

- `files` An array of file entries referenced by the source package; each entry has a `filename`, `size`, and `md5sum`.

#### Example:

```
{
  "files": [
    {
      "filename": "jake_1.0.orig.tar.bz2",
      "size": 1108,
      "md5sum": "a7a309b55424198ee98abcb8092d7be0"
    },
    {
      "filename": "jake_1.0-7.debian.tar.gz",
      "size": 1571,
      "md5sum": "0fa5395e95ddf846b419e96575ce8044"
    }
  ]
}
```

#### See Also:

The [docs](#resource_packages_method_contents) on the Package Contents API.
