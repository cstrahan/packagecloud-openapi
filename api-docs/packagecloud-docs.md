<a id="packages"></a>

## Packages

<a id="what_is_package"></a>

### What is a package?

A **package** is a combination of **metadata**, **configuration**, and **software** that is prepared in a way that a package management program (for example: [apt](https://help.ubuntu.com/community/Repositories/CommandLine) on Ubuntu, [yum](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/5/html/Deployment_Guide/c1-yum.html) on Red Hat Enterprise Linux, [pip](https://pip.pypa.io/) for Python packages and [gem](http://guides.rubygems.org/) for RubyGems) can use to properly and reliably install software and related configuration data on a computer.

<a id="why_packages_useful"></a>

### Why are packages useful?

- Version information helps keep software up to date.
- Metadata offers **visibility** in to what's installed where and why.
- **Reproducibility**: software is installed the same way, everywhere.

<a id="how_to_create_packages"></a>

### How do I create packages?

There are many tools for creating packages. Some tools are provided directly by Linux distributions. There are also many great third-party tools.

Some popular tools that can be used to create packages:

- [rpmbuild](http://wiki.centos.org/HowTos/SetupRpmBuildEnvironment) for RPM packages. Also, take a look [at this](https://fedoraproject.org/wiki/How_to_create_a_GNU_Hello_RPM_package) tutorial.
- [debuild](https://wiki.debian.org/IntroDebianPackaging) (includes an excellent tutorial) for DEB packages.
- [distutils](https://docs.python.org/2/distutils/builtdist.html) for Python packages.
- [gem](http://guides.rubygems.org/make-your-own-gem/) (includes an excellent tutorial) for RubyGems.

Advanced and third-party tools:

- [mock](http://fedoraproject.org/wiki/Using_Mock_to_test_package_builds) a chroot-based system for building RPM packages in a clean room environment.
- [pbuilder](https://wiki.ubuntu.com/PbuilderHowto) a chroot-based system for building DEB packages in a clean room environment. [This page](http://www.netfort.gr.jp/~dancer/software/pbuilder-doc/pbuilder-doc.html) also includes some useful tips about pbuilder.
- [git-buildpackage](http://honk.sigxcpu.org/projects/git-buildpackage/manual-html/gbp.html) a set of scripts that can be used to build DEB packages directly from git repositories.
- [fpm](https://github.com/jordansissel/fpm) a third-party tool that allows users to quickly and easily make a variety of packages (including RPM and DEB packages).
- [packpack](https://github.com/packpack/packpack) a simple tool to build RPM and Debian packages from git repositories.

<a id="which_types_of_packages"></a>

### Which types of packages does [packagecloud.io](https://packagecloud.io/) support?

Currently [packagecloud.io](https://packagecloud.io/) supports:

- RPM packages
- DEB packages
- Debian source packages (DSCs)
- Java packages (Clojure, SBT, "fatjar")
- Python packages (wheels, eggs, source distributions)
- RubyGems
- Node.js packages
- Alpine
- Generic files, e.g., .asc (e.g., signature files), .zip, etc.

<a id="repos"></a>

## Repos

<a id="what_is_a_repo"></a>

### What is a repo?

A repo (also known as 'repository') is a collection of [packages](#what_is_package) and some metadata describing a variety of attributes about the packages (for example: package versions, operating system version, dependencies, processor architecture, etc).

<a id="what_is_a_pkgcloud_repo"></a>

### What is a packagecloud repo?

A packagecloud repo is a more advanced take on the traditional repo.

A single packagecloud repo can:

- Contain packages of any (or all!) supported types; for example Debian, RPM, RubyGem, and Python packages can all coexist in the same packagecloud repo.
- Have packages for multiple Linux distributions; for example, if you have a Debian package that works for 2 versions of Ubuntu and 1 version of Debian you only need 1 packagecloud repo (see [pushing packages](#push_pkg) for more info).
- Issue [read tokens](#read_tokens) to identify specific nodes and control access to a repo by specific node.

<a id="why_are_repos_useful"></a>

### Why are [repos](#what_is_a_repo) useful?

Repos are useful because they:

- Allow you store several versions of the same package (useful for debugging purposes, security analysis, etc).
- Typically include some verification mechanism (like [GPG](#gpg)).
- Offer a way for many remote machines to download and install the same packages.
- Provide a way for software vendors to offer stable releases of software to customers.

<a id="how_to_create_repos"></a>

### How do I create [repos](#what_is_a_repo)?

There are a few open source tools that you can use to create a repo. Some of the mostly commonly used tools are:

- [createrepo](http://createrepo.baseurl.org) or [createrepo\_c](https://github.com/rpm-software-management/createrepo_c) for creating and managing RPM package repos (also called YUM repos).
- [reprepro](https://wiki.debian.org/DebianRepository/SetupWithReprepro) for creating and managing DEB package repos (also called APT repos).
- [gem](https://guides.rubygems.org/run-your-own-gem-server/) for creating and managing RubyGem servers.

Unfortunately, many of these tools are buggy, poorly documented, or difficult to use in production.

An excellent alternative is [packagecloud.io](https://packagecloud.io/) ;) - you can read more about how to create repos with our command line tool [here](#create_repo). You can also create repos on [packagecloud.io](https://packagecloud.io/) by logging in and clicking the **New Repository** button or by clicking [here](https://packagecloud.io/repositories/new).

We also have a walkthrough video demonstrating the repository creation process [that can be viewed here.](https://youtu.be/yS375M2CN8E)

<a id="disable_filelists"></a>

### Disabling filelists metadata

APT and YUM repositories have metadata which contains a list of every file in every package. This metadata can be used by users to query a given a filename and determine which package wrote that file to the filesystem.

The major downside of this feature is that repositories with huge numbers of packages or packages with huge numbers of files (like Omnibus packages) will have extremely large file list metadata. This can cause long wait times for clients because their apt and yum clients will download this metadata to the system when refreshing the cached metadata for a repository. This excessive metadata download can also increase the length of configuration management runs and take up significant space on the user's disk.

In order to deal with this, repository owners can click the 'edit' link to the right of their repository on their homepage and check the checkbox which says "Disable filelist metadata". Save your changes by clicking update. This will trigger a re-index for your repository and your contents metadata will be empty.

*NOTE: A package may check for dependency on another package by checking the existence of a file in the 'filelist metadata' of that other package. You should turn 'filelist metadata' back on if they encounter dependency issues.*

<a id="debian_component_support"></a>

### Debian repository component support

Since we make it easy to create and manage [as many repositories as you want](#how_to_create_repos), we feel there is no real need to support Debian repository components.

<a id="security_features"></a>

## Security Features

<a id="gpg"></a>

NOTE: The security features explained below are features that our product provides to ensure secure integration with existing tools and industry standard client software. These features are provided in our cloud based multi-tenant product as part of our standard offering.

### GPG keys

A [GPG](http://en.wikipedia.org/wiki/GNU_Privacy_Guard) key can be used to generate a [digital signature](http://en.wikipedia.org/wiki/Digital_signature) (read more about how [GPG generates and verifies digital signatures](http://gnupg.org/gph/en/manual/x135.html)).

Many package manage systems that come with Linux support two different types of GPG signatures. GPG signatures on packages themselves and GPG signatures on repository metadata. The distincition is very subtle, but very important.

### GPG signed packages

If you want to GPG sign your packages, you should do so before uploading it to packagecloud. packagecloud **does not** modify your uploaded data in anyway, whatsoever. If you sign your packages before uploading them, they will be signed when downloaded.

packagecloud allows repository owners to upload the GPG key used to sign the packages in a repository. When you do this, the key URL will be included in the package manager config that is generated for the client host. This ensures the key will be downloaded, added to the keyring, and used to verify package signatures. Note that packagecloud only stores public keys. If you happen to upload a secret key, we'll discard the secret key data and store only the public key when we process your GPG key upload.

### GPG signed repository metadata<a id="gpg_signing"></a>

packagecloud **does** GPG sign repository metadata that we generate for your repository. We do this to ensure to our users that your repository metadata was generated by us.

If you've installed your packagecloud repository using the Bash script, Chef cookbook, or Puppet module there is nothing extra you need to do. All of those methods automatically install the correct GPG key for your repository.

### Adding and removing GPG keys

For more information about adding or removing the GPG keys for a repository, visit the repository's page and click GPG. Read the next section to learn about how to export a GPG key that you've used to sign your packages so it can be uploaded to packagecloud.

### Exporting GPG keys

To export a GPG key that you've used to sign packages uploaded to packagecloud, follow these instructions.

1. Begin by running `gpg --list-keys --keyid-format=long`. This will print information about each GPG key in your keyring. It will look like this:

   ```

   pub   2048R/F2BB309992AE12C3 2015-03-14
   uid                          Fake Name (test key)
   sub   2048R/5F042FCD59BF0D31 2015-03-14

   ```
2. Find the key ID for the package signing key you are using. In the example above, the key ID is `F2BB309992AE12C3`.
3. Export the public key by running: `gpg --armor --export keyid`, substituting `keyid` for your GPG key ID.
4. Copy and paste this output into the package key dialog located in the Package signing key section of the GPG tab on your repository.

**Note** that if you accidentally upload a secret key, packagecloud will extract the public key and discard your secret key. **We never store your secret key** data even if uploaded to us accidentally.

### Learn more

To learn more about the technical inner workings of GPG signing packages vs repository metadata, check out our blog posts about [GPG signing and verifying Debian packages and APT repositories](https://blog.packagecloud.io/how-to-gpg-sign-and-verify-deb-packages-and-apt-repositories/) and

### GPG key migration

Some users have received notifications that they must migrate their repositories to
a new GPG key. This does not affect all repositories; only repositories created
prior to our new GPG key system being rolled out are affected.

#### Legacy GPG keys

In the early days of packagecloud, the service used a global GPG key to sign the
repository metadata generated for all APT and YUM repositories created.

This method works, but is a bit inflexible. Soon after we migrated to a new system
which uses [AWS Key Management Service](https://aws.amazon.com/kms/) to
generate GPG signing keys per-repository.

#### Per-repository GPG keys

Whenever a repository is created on packagecloud,
a new GPG key is generated specifically for that repository to be used for signing
repository metadata.

We are now migrating all repositories that were created before this system was rolled
out over to this new system. Any repositories created after are fine as is and no
action is required.

#### How to migrate

The migration can be performed in stages and we encourage affected users to click the
GPG tab on their repository page to more information on how to perform the migration.

Any repository that is not migrated will be automatically migrated on January 7, 2019.

<a id="https"></a>

### HTTPS

Both [public and private repos](#public_private_repos) have their metadata and package files served up over [HTTPS](http://en.wikipedia.org/wiki/HTTP_Secure) to prevent [MITM](http://en.wikipedia.org/wiki/Man-in-the-middle_attack) attacks.

packagecloud [repo install scripts](#install_repo) explicitly turn on certificate verification when possible.

<a id="public_private_repos"></a>

### Public / Private Repos

packagecloud allows you to create as many public repos as you like. Depending on your [plan](https://packagecloud.io/pricing) you may also be able to create private repos, as well.

**Public repos** are:

- Read accessible by anyone.
- Best suited for companies and individuals who are intending to distribute open source software.
- The repo owner and the specified [collaborators](#collaborators) may push packages to the repo.

**Private repos** are:

- Read accessible only with a read token
- Best suited for companies and individuals who have proprietary software.
- The repo owner and the specified [collaborators](#collaborators) may push packages to the repo.

<a id="collaborators"></a>

### Collaborators

packagecloud allows you to authorize other packagecloud users to [push](#push_pkg) packages to and [yank](#yank_pkg) packages from your
repos, as well as [promote](#promote_pkg) packages to other repositories.

You can add or remove collaborators by clicking the **edit** link found next to a repo name when you log in to packagecloud.

<a id="alpine"></a>

## Alpine

<a id="alpine_any"></a>

### Pushing and installing alpine\_any packages

---

#### About alpine\_any packages

Alpine packages, uploaded as alpine\_any, can be created to work on any alpine distro. This allows for a single package for every version, which can serve for all alpine-based Linuxes.

### Pushing a package using the CLI:

You can push a alpine alpine\_any/alpine\_any package [using the packagecloud CLI](https://www.rubydoc.info/gems/package_cloud/), like so:

```

package_cloud push <username>/<reponame>/alpine_any/alpine_any <alpine file>
```

### Using the alpine\_any/alpine\_any repo for installation:

1. Create a repo definition pointing to the alpine\_any/alpine\_any repo on packagecloud, and store it in `/etc/apk/repositories/`. Example:

   ```
   /etc/apk/repositories
   ```

   Alpine repository definitions like this can be added to the file:

   ```

       https://packagecloud.io/username/reponame/alpine_any/alpine_any/main

   ```
2. Update and get the metadata for the alpine\_any/alpine\_any repo on packagecloud. This command below will pull in the packages available on the repo you defined.

   ```
   apk update
   ```
3. Confirm the metadata from the repo you added by running:

   ```
   ls -ltr /var/cache/apk/
   ```

   The content should show as many APKINDEX.xxxxxx.tar.gz files as there are repositories in /etc/apk/repositories, with current date/time
4. Confirm the package you want is coming from the repo you defined:

   ```
   apk policy <package name>
   ```
5. Install the desired package with `apk add`:

   ```
   apk add <package name>
   ```

<a id="rpm"></a>

## RPM

<a id="rpm_any"></a>

### Pushing and installing rpm\_any packages

---

#### About rpm\_any packages

RPM packages, uploaded as rpm\_any, can be created to work on any rpm distros. This allows for a single package for every version, which can serve for all rpm-based Linuxes.

### Pushing a package using the CLI:

You can push a rpm rpm\_any/rpm\_any package [using the packagecloud CLI](https://www.rubydoc.info/gems/package_cloud/), like so:

```

package_cloud push <username>/<reponame>/rpm_any/rpm_any <rpm file>
```

### Using the rpm\_any/rpm\_any repo for installation:

1. Create a repo definition pointing to the rpm\_any/rpm\_any repo on packagecloud, and store it in `/etc/yum.repos.d/`. The filename MUST have the extension `.repo`. Example:

   ```
   /etc/yum.repos.d/username_reponame_rpm_any.repo
   ```

   The file content should be:

   ```

       [username_reponame_rpm_any]
       name=username_reponame_rpm_any
       baseurl=https://packagecloud.io/username/reponame/rpm_any/rpm_any/$basearch
       repo_gpgcheck=1
       gpgcheck=0
       enabled=1
       gpgkey=https://packagecloud.io/username/reponame/gpgkey
       sslverify=1
       sslcacert=/etc/pki/tls/certs/ca-bundle.crt
       metadata_expire=300
   ```
2. Update and get the metadata for the rpm\_any/rpm\_any repo on packagecloud. This command below will pull in the packages available on the repo pointed to by `username_reponame_rpm_any`, and you will be prompted to accept the GPG key of the repo.

   ```
   yum update --disablerepo=* --enablerepo=username_reponame_rpm_any
   ```
3. Confirm all available packages from the repo you added by running:

   ```
   yum list | grep username_reponame_rpm_any
   ```
4. Install the desired package with `yum install` or the below command, which will ensure you will install the package only from the repo pointed to by `username_reponame_rpm_any`

   ```
   yum install <package name> --disablerepo=* --enablerepo=username_reponame_rpm_any
   ```

Questions? We're here to help! Email [support@packagecloud.io](mailto:support@packagecloud.io)

<a id="deb"></a>

## Deb

<a id="deb_any"></a>

### Pushing and installing deb any/any packages

---

#### About deb any/any packages

Deb packages, uploaded as deb any/any, can be created to work on any deb distros. This allows for a single package for every version, which can serve for all deb-based Linuxes.

### Pushing a package using the CLI:

You can push a deb any/any package [using the packagecloud CLI](https://www.rubydoc.info/gems/package_cloud/), like so:

```
package_cloud push <username>/<reponame>/any/any <deb file>
```

### Using the any/any repo for installation:

1. Create a repo definition pointing to the any/any repo on packagecloud, and store it in `/etc/apt/sources.list.d/`. The filename MUST have the extension `.list`. Example:

   ```
   /etc/apt/sources.list.d/username_reponame_deb_any.list
   ```

   The file content should be:

   ```

       deb https://packagecloud.io/username/reponame/any/ any main
       deb-src https://packagecloud.io/username/reponame/any/ any main
   ```
2. Update and get the metadata for the any/any repo on packagecloud. This command will pull in the packages available on the repo pointed to by `username_reponame_deb_any`.

   ```

       sudo apt-get update \
       -o Dir::Etc::sourcelist="sources.list.d/username_reponame_deb_any.list" \
       -o Dir::Etc::sourceparts="-" \
       -o APT::Get::List-Cleanup="0"
   ```
3. Confirm the metadata from the repo you added by running:

   ```
   ls /var/apt/lists/
   ```

   The content should display the following:

   ```
   packagecloud.io_username_repo_any_dists_any_InRelease
   ```
4. Review which repo the package is coming from:

   ```
   apt-get install --print-uris <package name>
   ```
5. Install the desired package:

   ```
   apt-get install <package name>
   ```

<a id="rubygems"></a>

## RubyGems

<a id="bundler"></a>

### Bundler

### Adding the packagecloud repository to your Gemfile

---

#### Bundler 1.7.0 and above

In newer bundler versions, you can scope specific gems to a source, like so:

### public repos:

For public repositories, you'll only need to add it as a source to your Gemfile.

```

# Gemfile
#
# Note: It's recommended you add the official https://rubygems.org source, unless your
#       packagecloud repository can meet all of the dependency requirements in the Gemfile.

source "https://rubygems.org"
source "https://packagecloud.io/user/publicRepo" do
  gem "my-gem"
  gem "another-gem"
end
```

### private repos:

To install gems from a private repository, you'll need to add it as a source to your Gemfile with a read token. See [generating read tokens](#generate_read_token).

```

# Gemfile
# Replace ${token} with a valid read token

source "https://rubygems.org"
source "https://${token}:@packagecloud.io/user/privateRepo" do
  gem "my-private-gem"
  gem "another-private-gem"
end
```

### Legacy versions of Bundler

Older versions of Bundler have several bugs around scoping gems to a single source using blocks, so you'll have to add the source globally at the top of the Gemfile.

### public repos:

```

# Gemfile

source "https://rubygems.org"
source "https://packagecloud.io/user/publicRepo"
```

### private repos:

```

# Gemfile
# Replace ${token} with a valid read token.

source "https://rubygems.org"
source "https://${token}:@packagecloud.io/user/privateRepo"
```

<a id="python"></a>

## Python

<a id="venv"></a>

### VirtualEnv

### Adding the repository to your VirtualEnv

Ensure you are running the latest version of pip inside your virtualenv:

```
my_virtualenv/bin/pip install --upgrade pip
```

### public repos:

Add this to the bottom of your `requirements.txt`

```
--extra-index-url=https://packagecloud.io/user/publicRepo/pypi/simple
```

### private repos:

Append the repository to `requirements.txt` using a read token. Replace `${token}` with your generated read token. See [generating read tokens](#generate_read_token).

```
--extra-index-url=https://${token}:@packagecloud.io/user/privateRepo/pypi/simple
```

*Note: if you would like pip to use **only** this repository as a source, replace `extra-index-url` with `index-url`*

<a id="node"></a>

## NodeJS

<a id="node_npm"></a>

### Configure an npm registry

<a id="npm_set_repository_url"></a>

Use the `npm config set registry <url>` command to set the npm registry for your system.

This command will create an `.npmrc` file with the custom registry url in the current user's home directory.
The `url` should be a fully-qualified url to a packagecloud repository and **must** include the trailing `npm/`.

For example, to set the npm registry to `example-user`'s repository named `example-repo`,
you would run the following command:

```
https://packagecloud.io/example-user/example-repo/npm/
```

Follow the directions in the next sections to set up [read-only access](#npm_read_only) or
[read and write access](#npm_read_and_write) to the repository.

<a id="npm_read_only"></a>

### Read only access to npm repositories

#### Public npm repositories

If the repostory is a public repository, your system will have read access to the repository after running `npm config set registry <url>`
as described in the previous section.

You can install packages by simply running `npm install [packagename]`.

#### Private npm repositories

To configure read only access to a private npm registry, use the repository installation scripts which can be found
in the Installation section on a repository page.

Alternatively, you can create a [read token](#read_tokens) and and set the `_authToken` manually by editing the `.npmrc` file
in your user's home directory.

*`.npmrc` file:*

```
https://packagecloud.io/example-user/example-repo/npm/
```

*Note: The registry url **must** end in **/npm/***

The `_authToken` must be a valid [read token](#read_token) generated from a repository [master token](#master_tokens). Learn more about [read tokens](#read_tokens) in these docs.

The `always-auth` field is required when using **[Yarn](#node_yarn)** with a private repository.

<a id="npm_read_and_write"></a>

### Read and write access to npm repositories

You should only follow these instructions on systems and environments where you need write access to your repository. If you just need
to run `npm install` to install packages, you should follow the [read only access guide](#npm_read_only) above.

<a id="npm_login"></a>

#### npm login

After you have set your repository URL by following [the guide above](#npm_set_repository_url), you
are ready to use `npm login` to give yourself write access to the repository.

Start by using the `npm login` command. Running this command
will modify the `.npmrc` file in your home directory to include an authentication token that has write access.

When running the `npm login` command, you will be prompted for a username, password, and email address.
Use your packagecloud account name, your packagecloud account password, and packagecloud account email address, respectively.

For example, if your packagecloud username is `example-user` and the email address registered to your account is
`example-user@company.com`, you would run `npm login` and respond like this:

```

~/Projects/example-project $ npm login
Username: example-user
Password: **************
Email: (this IS public) example-user@company.com
Logged in as example-user on https://packagecloud.io/example-user/example-repo/npm/.
```

<a id="npm_publish"></a>

#### npm publish

After you have followed the [npm login](#npm_login) section above, you
are ready to use `npm publish`.

Use the `npm` cli to publish packages to your packagecloud registry.
Run `npm publish <tarball>` or `npm publish`
from inside a project root containing a `package.json` to publish
packages to a configured registry.

You can also use the [packagecloud CLI](#cli), API, or web
interface to upload packages to the npm registry.

<a id="node_scoped"></a>

### Scoped packages

Scoped packages are supported on packagecloud. Install scoped packages by including the scope in the package name.

```

npm install @example/package
```

Publishing scoped packages is also supported. Use the `npm publish` command, packagecloud CLI, or web UI to upload packages.
Ensure the scope is included in the package name field inside the `package.json`.

```

npm publish example-package-v0.1.0.tgz
```

<a id="node_unpublish"></a>

### Remove / unpublish packages from the registry

To remove packages from your packagecloud registry, you can use the [packagecloud CLI](#cli) or the API directly to delete the package.

CLI Example:

```

package_cloud yank example-user/example-repository/node example-1.0.tgz
```

To remove scoped packages from your packagecloud registry, you pass the scope to the CLI, like so:

```

package_cloud yank example-user/example-repository/node @myuser/example-1.0.tgz
```

You can also delete packages from the web UI by visiting the repository page, selecting the package you want to delete, and choosing delete from the options presented. Deleting the package will trigger a reindex of the registry metadata.

<a id="npm_proxy"></a>

### Transparent auto-proxying

When you install a package using `npm install`, the `npm` program will automatically
attempt to install any dependencies required by the package. If those dependencies are not found in your
packagecloud repository, packagecloud will automatically forward requests for those missing dependencies to the official
npm public registry.

This is the default behavior and is recommended for most users.

If you do not want to rely on the official npm public registry at all, you can disable the automatic forwarding
of requests. However, once this behavior is disabled, you will need to upload your packages and all
required dependencies to your packagecloud repository. To disable automatic proxying to the
official npm public registry for missing dependencies, visit the settings page for the repository and
uncheck the "Enable proxying from the official npm registry" checkbox.

If you decide to disable this behavior, you will have to upload *every*
dependency for *every* package you upload. `npm install` commands
will fail if any dependencies are missing from your packagecloud repository
because `npm install` will no longer be able to rely on the
official npm public registry.

<a id="node_yarn"></a>

### Using Yarn

Once a system is configured to use a packagecloud repository as an npm registry, either by following the manual installation instructions, or by using the repository install scripts provided by packagecloud, it can install packages via **Yarn** by using `yarn add <packagename>`. No other configuration is necessary.

```
yarn add packagename@0.1.0
```

<a id="dist_tags"></a>

### npm dist tags

npm supports a useful feature called distribution tags (or dist tags) for short. You can learn about
[dist tags by reading the npm documentation](https://docs.npmjs.com/getting-started/using-tags).

Please read the important notes about dist tags in the sections that follow. The behavior of dist tags with
package publish, promote, and delete may not be what you expect!

In short, npm dist tags allow npm package owners to associate arbitrary strings with npm package versions.
All packages have at least one dist tag: the "latest" dist tag. The "latest" dist tag is automatically
set to the most recently uploaded version of a package. When you run `npm install package`, your npm
command line client automatically installs the version tagged with "latest".

You can create arbitrary dist tags (for example: alpha, beta, testing, stable, etc) that map to
particular versions of a package. A user can then use that dist tag to install the version of a package mapped
to that tag.

For example: you may decide that version 2.0 of example-package is the current beta version, so you create
a dist tag mapping "beta" to version 2.0. Any user who wants to install the beta, can simply run
`npm install example-package@beta`.

The npm API for adding, removing, and listing [dist tags](https://docs.npmjs.com/getting-started/using-tags)
is fully supported by packagecloud. This means you can run commands like: `npm dist-tag ls package-name` or
`npm dist-tag add package-name@2.0 beta` to list or add dist tags, respectively.

<a id="node_publish"></a>

### Publishing a package and distribution tags (dist tags)

In order to maintain API compatibility with the official npm registry and its API you should be be aware that
when uploading a Node.js package with the:

- Web-based graphical upload dialog, the package uploaded will be marked as
  the latest version *regardless* of its version string.
- [package\_cloud command
  line client](#cli), the package uploaded will be marked as the latest version *regardless* of its version string.
- `npm publish` command without specifying a distribution tag,
  the newly published package will be marked as the latest version *regardless* of its version string.
- `npm publish` command and also specifying a distribution tag
  using the `--tag` option, the newly published package will be marked with the specified dist tag. The "latest"
  distribution tag will remain unchanged and will be set to whichever version it was set to (if any).

You can add, remove, or list dist tags using the
[npm dist-tags command](https://docs.npmjs.com/getting-started/using-tags)
to modify the dist tags, manually.

<a id="node_promote"></a>

### Node package promotion and distribution tags (dist tags)

When you [promote a package](#promote_pkg), the package is removed from the source repository and exists
only in the destination repository at the completion of the command.

When a Node.js package is promoted, the follow things occur:

1. All distribution tags associated with that package are **deleted**.
2. The remaining versions of the package in the original repository (where the package was moved from) will be sorted
   according to the version. The most recent version string is marked as the latest (even if it already has another dist tag).
3. Once the package reaches the destination repository, it will be marked as latest if (and only if) no other versions of the same package
   exist at the destination. If other versions exist, the version that was just moved has no dist tag associated with it, even if the
   semantic version is the latest.

This is done to mimic the official npm repository as closely as possible. You can use the
[npm dist-tags command](https://docs.npmjs.com/getting-started/using-tags)
to create, remove, or adjust any dist tags you need after promoting a package.

<a id="node_delete"></a>

### Node package deletion and distribution tags (dist tags)

When you [delete (or yank) a Node.js package](https://packagecloud/docs#yank) the version strings of all remaining
versions for that package are sorted and the most recent version is marked as "latest" even if there is already another dist tag associated
with that version. This is done to maintain API compatibility with the official npm registry and its API.

## Helm

<a id="helm"></a>

### Configure Helm repository

<a id="helm_set_repository_url"></a>

Use `helm repo add <reponame> <url>` command to set the Helm repository for your system.

`<reponame>` can be anything of your choice and has significance only our your system.

This command will create a `repositories.yaml` file with the custom registry url in:

- Linux: $HOME/.config/helm
- MacOS: $HOME/Library/Preferences/helm
- Windows: %APPDATA%\helm

The `url` should be a fully-qualified url to a packagecloud repository and **must** include the trailing `helm/`.

For example, to set the Helm repository to `example-user`'s repository named `example-repo`,
you would run the following command:

```
https://packagecloud.io/example-user/example-repo/helm/
```

### Public Helm repositories

If the repostory is a public repository, your system will have read access to the repository after running `helm repo add <reponame> <url>` as described in the previous section.

You can install charts by simply running `helm install [release_name] [package_name]`.

### Private Helm repositories

To configure read only access to a private Helm registry, use the repository installation scripts which can be found
in the Installation section on a repository page.

Alternatively, you can create a [read token](#read_tokens) and and set the `_authToken` manually use `helm repo add --password <password> <reponame> <url>`

The `_authToken` must be a valid [read token](#read_token) generated from a repository [master token](#master_tokens). Learn more about [read tokens](#read_tokens) in these docs.

<a id="helm_unpublish"></a>

### Remove / unpublish packages from the registry

To remove packages from your packagecloud registry, you can use the [packagecloud CLI](#cli) or the API directly to delete the package.

CLI Example:

`v1` is the index version

```

package_cloud yank example-user/example-repo/helm/v1 example-1.0.tgz
```

You can also delete packages from the web UI by visiting the repository page, selecting the package you want to delete, and choosing delete from the options presented. Deleting the package will trigger a reindex of the registry metadata.

<a id="helm_promote"></a>

### Helm package promotion

When you [promote a package](#promote_pkg), the package is removed from the source repository and exists
only in the destination repository at the completion of the command.

CLI Example:

`v1` is the index version

```

package_cloud promote example-user/example-repo/helm/v1 example-1.0.tgz target-user/target-repo
```

<a id="token_auth"></a>

## Token Auth

We support a sophisticated multi-level authentication system that facilitates a wide variety of use cases for private repos. There are three different kinds of tokens: [master tokens](#master_tokens), [read tokens](#read_tokens) and [API tokens](https://packagecloud.io/docs/api#api_tokens).

<a id="token_capabilities"></a>

### Token Capabilities

|  | Create Read Tokens | Read Repository Metadata\* | Download Packages | Upload Packages | Use Case |
| --- | --- | --- | --- | --- | --- |
| [Read Tokens](#read_tokens) | No | Yes | No | No | Package Managers |
| [Master Tokens](#master_tokens) | Yes | No | No | No | Creating [Read Tokens](#read_tokens) |
| [API Tokens](https://packagecloud.io/docs/api#api_tokens) | Yes | No\*\* | Yes | Yes | Automation |

*\* This includes downloading packages made available through repository metadata.*

*\*\* For compatibility with the npm tool, API tokens can [read and write to npm registries](#npm_read_and_write).*

<a id="master_tokens"></a>

### Master Tokens

Master tokens are at the top level and **their only purpose is generating descendent read tokens**.

Master tokens can't be used for reading from repos, pushing packages, modifying configurations, or doing anything else. **That means that you can safely give master tokens to customers, embed them in configuration management manifests, or otherwise distribute them to untrusted parties.**

Each repo comes with a default master token. If you don't have a need for maintaining fine-grained access control to your repos, then all packagecloud functionality will automatically use the default master token transparently to you.

Master tokens can be generated and destroyed with the [package\_cloud command line client](#cli). For example, to create a new token named test, you would run the following command:

```
> package_cloud master_token create username/reponame master_token_name
```

<a id="read_tokens"></a>

### Read Tokens

Read tokens are what's used to authenticate against the packagecloud repository. In other words, the package manager on your system will send this token along with its requests for repo metadata and packages.

These tokens are **read-only**, meaning that they can't be used to modify the repo in any way or authenticate against any packagecloud endpoints aside from the package servers themselves.We recommend using one read token per node to maximize isolation.

Read tokens are generated automatically by our [repo installation scripts](#install_repo). Our scripts automatically associate read tokens with a node's hostname. If you write your own config management manifests, generating and associating read tokens is a simple matter of making a call to a REST API.

<a id="revocation"></a>

### Revocation

If you want to revoke access to one node at a time, you can revoke its read token using the CLI. This is one of the benefits of generating one read-token per node.

NOTE: Use the master token name and read token name NOT the actual token values

```
> package_cloud read_token destroy username/reponame master_token_name/read_token_name
```

By revoking a master token, you can revoke all of its read token descendents at once, making it straightforward to — at once — revoke an entire customer, datacenter, or other logical grouping that exists in your system.

NOTE: Use the master token name NOT the actual token value

```
> package_cloud master_token destroy username/reponame master_token_name
```

<a id="generate_read_token"></a>

### Generating a Read Token for Private Repo Access

Generating a read token is a matter of making a REST call to the tokens endpoint for your repository. The following example will generate and return a read token for the private repository.

The `${master_token}` in the example is referring to the master token associated to a repository. See [Master Tokens](#master_tokens).

**NOTE: The installation scripts provided by packagecloud automatically generate read tokens for private repositories when they're executed. Take a look at the installation instructions for any packagecloud repository.**

```
UNIQUE_ID=`hostname -f` && curl -XPOST --data "name=${UNIQUE_ID}" https://${master_token}:@packagecloud.io/install/repositories/${username}/${repository}/tokens.text
```

<a id="ci"></a>

## Continuous Integration

<a id="circle_ci"></a>

### CircleCI

To push packages to packagecloud from [CircleCI](https://circleci.com/) you must:

1. Set an environment variable named `PACKAGECLOUD_TOKEN` in your project's settings and the value must match your packagecloud [API access token](https://packagecloud.io/api_token).
2. Create a circle.yml file which installs the package\_cloud gem and [pushes the package](#push_pkg) to the [OS and version of your choice](#os_distro_version).

For more info on your API access token, please refer to the API Tokens section in [API docs](https://packagecloud.io/docs/api#api_tokens).

Just an example; get your real API token [here](https://packagecloud.io/api_token).

```
PACKAGECLOUD_TOKEN: f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0
```

Example circle.yml file

```

dependencies:
  pre:
    - gem install package_cloud

deployment:
  production:
    branch: master
    commands:
      - package_cloud push user/repo/os/version /path/to/pkg.ext
```

<a id="travis"></a>

### Travis CI

To push packages to packagecloud from Travis CI you must:

1. Set an environment variable named `PACKAGECLOUD_TOKEN` in your project's settings and the value must match your packagecloud [API access token](https://packagecloud.io/api_token).
2. Create a .travis.yml file which installs the package\_cloud gem and [pushes the package](#push_pkg) to the [OS and version of your choice](#os_distro_version).

For more info on your API access token, please refer to the API Tokens section in [API docs](https://packagecloud.io/docs/api#api_tokens).

Just an example; get your real API token [here](https://packagecloud.io/api_token).

```
PACKAGECLOUD_TOKEN: f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0
```

Example .travis.yml file

```

before_install:
  - gem install package_cloud

script:
  - package_cloud push user/repo/os/version /path/to/package.ext
```

<a id="jenkins"></a>

### Jenkins

To push packages to packagecloud from Jenkins you'll need to install and configure the [packagecloud Jenkins plugin](https://wiki.jenkins-ci.org/display/JENKINS/Packagecloud+Plugin).

The step by step instructions can be found on the [packagecloud Jenkins plugin wiki page](https://wiki.jenkins-ci.org/display/JENKINS/Packagecloud+Plugin).

There are 3 steps to the configuration process:

1. [Plugin installation](https://wiki.jenkins-ci.org/display/JENKINS/Packagecloud+Plugin#PackagecloudPlugin-plugininstall): begin by finding and installing the Jenkins plugin via the Jenkins UI
2. [Credentials setup](https://wiki.jenkins-ci.org/display/JENKINS/Packagecloud+Plugin#PackagecloudPlugin-credssetup): next, use Jenkins' credentials system to store your packagecloud username and API token
3. [Configure post-build job](https://wiki.jenkins-ci.org/display/JENKINS/Packagecloud+Plugin#PackagecloudPlugin-uploadartifacts): finally, add a post-build step to your Jenkins job, enter the repository to push to, and select the operating system and version

You'll need to use your packagecloud username and API token when configuring credentials in Jenkins.

Please log in to packagecloud to view your username and API token.

<a id="buildkite"></a>

### Buildkite

To push packages to packagecloud from Buildkite you must:

1. Ensure the package\_cloud gem is installed in your agent environment
2. Expose the `PACKAGECLOUD_TOKEN` environment variable in your [Buildkite environment hook](https://buildkite.com/docs/agent/securing#using-environment-hooks-for-secrets)
3. Add a build script to push your build artifact to packagecloud

For more info on your API access token, please refer to the API Tokens section in [API docs](https://packagecloud.io/docs/api#api_tokens).

Just an example; get your real API token [here](https://packagecloud.io/api_token).

```
#!/bin/bash

export PACKAGECLOUD_TOKEN=f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0
```

Example build script that pushes a previously built build artifact to packagecloud:

```
#!/bin/bash

set -e

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 username/myrepo path/to/package/artifact"
  exit 1
fi

# Download package artifact from a previous build step
buildkite-agent artifact download "$1" .

# Push package to packagecloud
package_cloud push "$2" "$(basename $1)"

```

Example build pipeline:

![Buildkite user interface showing a step with a Packagecloud upload command](https://assets-production.packagecloud.io/assets/buildkite_w585_h379-02f3b63960cf079f0df0318572678a71ad251e98dfc30167235f0b9bd421b538.png)

<a id="github_actions"></a>

### GitHub Actions

NOTE: This video shows how to use the [GitHub Action](https://github.com/marketplace/actions/upload-package-packagecloud-io) generously created by our OSS customer, [Daniel](https://github.com/danielmundi) at [WLAN-Pi](https://www.wlanpi.com/) prior to our official one being developed. Please feel free to use it keeping in mind it is not maintained by Packagecloud.

**The steps on using the [official Packagecloud GitHub Action ('push-package-to-packagecloud-io')](https://github.com/marketplace/actions/push-package-to-packagecloud-io) to push packages is as follows.**

1. If needed, download the [GitHub CLI](https://cli.github.com/)
2. Create an encrypted secret named `PACKAGECLOUD_TOKEN` in your GitHub repository and set your packagecloud API token as the value.
Just an example - login and find your real API token [here](https://packagecloud.io/api_token).

```
gh secret set PACKAGECLOUD_TOKEN -b"f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0"
```

3. Create a .github/workflows directory
4. On the GitHub Actions page, click the 'Use latest version' button and copy the snippet to your .yml file in the above directory. (It can be named anything, for example: upload.yml.)
5. In that .yml file, copy and modify the appropriate fields below with your package name, username, repository to [push the package](#push_pkg) into, [OS/version of your choice](#os_distro_version) (if applicable), and API token.
Example:

```

      name: dev-ci
      on: [push]
      jobs:
        upload:
          runs-on: ubuntu-latest
          steps:
      ##### MODIFY: Add steps to build package or copy package to github action container
      #####         so it is available to github action to upload to packagecloud
            - name: push package to packagecloud.io
              uses: computology/packagecloud-github-action@v0.6
              with:
      ##### MODIFY: Change to packagecloud username, reponame, distro type
      #####         To understand the available distro type, see https://www.rubydoc.info/gems/package_cloud/#pushing-a-package
                PACKAGE-NAME: dist/*.tar.gz
                PACKAGECLOUD-USERNAME: test_user
                PACKAGECLOUD-REPONAME: test_repo
                PACKAGECLOUD-DISTRO: python
                PACKAGECLOUD-TOKEN: ${{ secrets.PACKAGECLOUD_TOKEN }}
```

6. Make a commit, push the file to your GitHub repository, and observe the workflow run under the 'Actions' tab from the GitHub UI.

<a id="build_tools"></a>

## Deploying from Build Tools

<a id="maven_deploy"></a>

### Maven Deploy

1. If you haven't already, add your [API token](https://packagecloud.io/api_token) to your local maven settings file located at `$HOME/.m2/settings.xml`.
   Optionally, you can encrypt these values for greater security,
   consult their [Password Encryption documentation](https://maven.apache.org/guides/mini/guide-encryption.html) for instructions.

   Login to packagecloud to view your username and API token.
2. Configure your project's `<distributionManagement>` to point to your
   packagecloud.io repository, making sure that the `<id>` matches the entry we created above with your token. (We are setting
   our `SNAPSHOT` and release repositories to the same repository, feel free to use different ones according to your needs).

   ```

   <distributionManagement>
     <repository>
       <id>packagecloud-myrepo</id>
       <url>https://packagecloud.io/test-user/myrepo/maven2</url>
     </repository>
     <snapshotRepository>
       <id>packagecloud-myrepo</id>
       <url>https://packagecloud.io/test-user/myrepo/maven2</url>
     </snapshotRepository>
   </distributionManagement>
   ```
3. Deploy your project to packagecloud!

   ```

   mvn deploy
   ```

<a id="lein_deploy"></a>

### Leiningen Deploy

Deploying artifacts using the [lein-maven-packagecloud-wagon](https://github.com/computology/lein-maven-packagecloud-wagon):

1. If you haven't already, add your [API token](https://packagecloud.io/api_token) to your local leiningen profiles file located at `$HOME/.lein/profiles.clj`.
   Optionally, you can encrypt these values for greater security, consult their [GPG documentation](https://github.com/technomancy/leiningen/blob/stable/doc/DEPLOY.md#gpg) for instructions.

   Login to packagecloud to view your username and API token.
2. Add the dependency to the `:plugins` section of your project's`project.clj`.

   ```

   :plugins [[lein-maven-packagecloud-wagon "0.0.1"]]
   ```
3. Configure your project's `:deploy-repositories` to point to your packagecloud.io repository. (We are setting
   our `SNAPSHOT` and release repositories to the same repository, feel free to use different ones according to your needs).

   ```

   :deploy-repositories [["releases" {:url "packagecloud-https://packagecloud.io/test-user/myrepo"}]
                         ["snapshots" {:url "packagecloud-https://packagecloud.io/test-user/myrepo"}]]
   ```
4. Deploy your project to packagecloud.io!

   ```

   lein deploy
   ```

<a id="gradle_deploy"></a>

### Gradle Deploy

Deploying artifacts using the [Gradle Maven Deployer](https://docs.gradle.org/current/userguide/maven_plugin.html)

1. If you haven't already, add your [API token](https://packagecloud.io/api_token) to your local gradle file located at `$HOME/.gradle/gradle.properties`.

   Login to packagecloud to view your username and API token.
2. Require the `maven` plugin in your project's`build.gradle`.

   ```

   apply plugin: 'maven'
   ```
3. Setup the `deployerJars` in the `configurations` section of your project's`build.gradle`.

   ```

   configurations {
       deployerJars
   }
   ```
4. Add the dependency to the `dependencies` section of your project's`build.gradle`.

   ```

   dependencies {
       deployerJars "io.packagecloud.maven.wagon:maven-packagecloud-wagon:0.0.6"
   }
   ```
5. Configure your project's `uploadArchives` to point to your packagecloud.io maven repository.

   ```

   uploadArchives {
       repositories.mavenDeployer {
           configuration = configurations.deployerJars
           repository(url: "packagecloud+https://packagecloud.io/test-user/myrepo") {
               authentication(password: mavenPassword)
           }
       }
   }
   ```
6. Deploy your project to packagecloud.io!

   ```

   gradle uploadArchives
   ```

#### NOTES:

**Android Studio/Gradle 4.x.x Users:** If you are getting errors like "Unable to detect maven coordinates (groupId, artifactId, version)..." while uploading, you'll need to define the coordinates explicitly inside of `uploadArchives`, like so:

```

uploadArchives {
    repositories.mavenDeployer {
        pom.groupId = 'com.my_group_id'
        pom.artifactId = 'myexamplelibrary'
        pom.version = '1.0.1-SNAPSHOT'
        configuration = configurations.deployerJars
        repository(url: "packagecloud+https://packagecloud.io/test-user/myrepo") {
            authentication(password: mavenPassword)
        }
    }
}
```

For SNAPSHOT support, just add `-SNAPSHOT` to your `version`.

You might see some "Could not find metadata: maven-metadata.xml" messages fly by; these are not errors and can safely be ignored.

<a id="gradle_maven_publish_deploy"></a>

### Gradle Maven Publish Deploy

Deploying artifacts using the [Gradle Maven Publish Plugin Deployer](https://docs.gradle.org/current/userguide/maven_plugin.html)

1. Require the `java` and `maven-publish` plugins in your project's `build.gradle`.

   ```

   ['java', 'maven-publish'].each {
       apply plugin : it
   }
   ```
2. Add your custom `group` and project `version`. For SNAPSHOT support, just add `-SNAPSHOT` to your `version`.

   ```

   group = 'io.packagecloud.sample'
   version = '1.0.0'
   repositories {
       gradlePluginPortal()
   }
   ```
3. Once the appropriate plugins have been applied, you can configure the publications and repositories. Don't forget to add your username and repository name into the `url`, paste your [API token](https://packagecloud.io/api_token) into `username` and leave `password` blank.

   ```

   publishing {
       publications {
           myPublication(MavenPublication) {
               // telling gradle to publish project's jar archive (2)
               from components.java
               // telling gradle to publish README file (2)
               // artifact ('README.txt') {
               //     classifier = 'README'
               //     extension  = 'txt'
               // }
           }
       }
       // telling gradle to publish artifact to repo (3)
       repositories {
           maven {
              url "https://packagecloud.io/test_user/test_repository/java/maven2/"
              credentials {
                  username = "<YOUR_API_TOKEN>"
                  password = ""
              }
           }
       }
   }
   ```
4. Deploy your project to packagecloud.io!

   ```

   ./gradlew publish
   ```

<a id="sbt_deploy"></a>

### SBT Deploy

To deploy artifacts using SBT, we'll be wrapping our [maven-packagecloud-wagon](https://github.com/computology/maven-packagecloud-wagon) with
the [aether-deploy](https://github.com/arktekk/sbt-aether-deploy) SBT plugin.

**NOTE:** You must have at least [SBT 0.13.8](http://www.scala-sbt.org/download.html) installed.

1. If you haven't already, add your [API token](https://packagecloud.io/api_token) to your local ivy credentials file located at `$HOME/.ivy2/.credentials`.

   Login to packagecloud to view your username and API token.
2. Add the plugin dependency to a `project/plugins.sbt` file in your project. (Create file if neccesary).

   ```

   addSbtPlugin("no.arktekk.sbt" % "aether-deploy" % "0.20.0")
   libraryDependencies += "io.packagecloud.maven.wagon" % "maven-packagecloud-wagon" % "0.0.6"
   ```

   **NOTE:** Only works with Java 8 or above, for Java 7 you'll have to use `"aether-deploy" % "0.17"`, which does not support SBT 1.1.x
3. Paste the following block of code towards the bottom of your `build.sbt` file. This configures the credentials path and sets
   the publishing destination for our artifacts.

   ```

   import aether.AetherKeys._

   credentials += Credentials(Path.userHome / ".ivy2" / ".credentials")

   aetherWagons := Seq(aether.WagonWrapper("packagecloud+https", "io.packagecloud.maven.wagon.PackagecloudWagon"))

   publishTo := {
     Some("packagecloud+https" at "packagecloud+https://packagecloud.io/test-user/myrepo")
   }
   ```
4. Deploy your project to packagecloud!

   ```

   sbt aether-deploy
   ```

<a id="maven-metadata"></a>

## Maven Metadata

Maven-metadata XML file stores information that can help software developers quickly understand the history and current state of their java artifacts and use this information to integrate their software with different tools.

<a id="where-to-maven-metadata"></a>

### Where to get it?

You can access the maven-metadata.xml file of a java package hosted in a public repository using the following URL pattern.

```
https://packagecloud.io/example-username/example-repository-name/maven2/example-group/example-package-name-without-version/maven-metadata.xml
```

If you want to access the maven-metadata.xml file of a java package hosted in a private repository you would need to pass the master token of that repository through the URL as shown in the following URL pattern.

```
https://packagecloud.io/priv/example-repository-master-token/example-username/example-repository-name/maven2/example-group/example-package-name-without-version/maven-metadata.xml
```

You can learn more about master tokens [here](#master_tokens).

NOTE: maven-metadata xml file will only be rendered if all the version names of your package comply with the Semantic Versioning [specifications](https://semver.org/).

<a id="cli"></a>

## Command Line Client

<a id="cli_install"></a>

You can find additional documentation about the packagecloud command line [here](http://www.rubydoc.info/gems/package_cloud/) and
by running package\_cloud help.

### Installation

Once you get the package\_cloud CLI tool installed, you can create repositories and push packages quickly and easily.

1. If you don't already have Ruby, you need to install it. You can find install instructions for most platforms [here](https://www.ruby-lang.org/en/documentation/installation/).
2. Install the package\_cloud Ruby gem by running:

   ```
   > sudo gem install package_cloud
   ```

The package\_cloud CLI has built-in help that can be accessed by running:

```
> package_cloud help
```

<a id="manual_pcloud_file"></a>

### Creation of .packagecloud file

`$HOME/.packagecloud` allows package\_cloud CLI to authenticate your session and check your permissions. There are two ways to set this file up

#### Manual creation

1. Go to <https://packagecloud.io/api_token> and copy the auto-generated settings.
2. Save the content into a new file in your `$HOME` directory.

   Just an example; get your real settings [here](https://packagecloud.io/api_token).

   ```
   echo '{"url":"https://packagecloud.io/", "token": "f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0"}'' >> ~/.packagecloud
   ```

#### Direct download

You can also download the configuration file directly from the site if you click the download button in <https://packagecloud.io/api_token>, don't forget to rename this file to .packagecloud and move it from your downloads to your `$HOME` directory.

<a id="create_repo"></a>

### Creating repos

There are two ways to create a new repo:

1. Using the web UI: <https://packagecloud.io/repositories/new>
2. Using the package\_cloud CLI:

   ```
   > package_cloud repository create myrepo
   ```

If your [plan](https://packagecloud.io/pricing) allows you to create private repos, you can create one by:

1. Selecting *Private* in the web UI on the repo create page: <https://packagecloud.io/repositories/new>
2. Passing a flag to the package\_cloud CLI:

   ```
   > package_cloud repository create myrepo --private
   ```

<a id="push_pkg"></a>

### Pushing packages

You can push a package using the package\_cloud CLI:

```
> package_cloud push username/myrepo /path/to/packagefile
```

Some package types can be associated to specific versions of particular Linux distributions. If the package type you are pushing needs to be associated with a particular version you will be prompted by the package\_cloud CLI.

You can also specify the version in the command line, for example, to push a package to Ubuntu 12.04 Precise, you would use:

```
> package_cloud push username/reponame/ubuntu/precise /path/to/packagefile
```

#### Supplying/Overriding Maven Coordinates

Sometimes (like for "fatjars"), we are unable to automatically detect the maven coordinates for a particular package, so you'll have to supply it on the command line like so:

```
> package_cloud push username/reponame/java /path/to/package.jar --coordinates=com.mygroup:packagename:1.0.2
```

#### Uploading multiple packages and skipping errors

You may upload an entire directory of packages using a glob:

```
> package_cloud push username/myrepo /path/*.rpm
```

If you attempt to re-run this command after additional packages to the directory, it will fail once it tries to upload a package that already exists. You can use the --skip-errors
flag to force the CLI to skip packages that that already exist and proceed to the next package:

```
> package_cloud push username/myrepo /path/*.rpm --skip-errors
```

<a id="yank_pkg"></a>

### Yanking packages (Delete a package)

You can remove a package from a repo by using the package\_cloud CLI:

```
> package_cloud yank username/myrepo/[distro/version] packagename.ext
```

The packagename.ext must be the full filename of the package, including the extension.

Some packages (RPMs, Debs, Python packages, Node.js, and JARs) are pushed to a specific distribution and version. When those packages are removed, the distribution and version that should be removed must be specified.

Other package types (RubyGems) can be removed without specifying a distribution or version, as these do not apply to RubyGem packages.

### Examples

Remove a package called jake-1.0-2.src.rpm from a CentOS 6 repo named myrepo:

```
> package_cloud yank username/myrepo/el/6 jake-1.0-2.src.rpm
```

Remove a package called redis\_2.8.1-1\_amd64.deb from an Ubuntu Precise (12.04) repo named myrepo:

```
> package_cloud yank username/myrepo/ubuntu/precise redis_2.8.1-1_amd64.deb
```

Remove a package called packagecloud\_test-0.0.1.whl from a Python repo named myrepo:

```
> package_cloud yank username/myrepo/python packagecloud_test-0.0.1.whl
```

Remove a package called passenger-4.0.43.gem from a RubyGem repo named myrepo:

```
> package_cloud yank username/myrepo passenger-4.0.43.gem
```

Remove a package called jake-2.3.jar with the group com.groupidfrom a Maven repo named myrepo:

```
> package_cloud yank username/myrepo/java com.groupid/jake-2.3.jar
```

Remove a package called packagecloud-1.0.1.tgz from an npm registry named myrepo:

```
> package_cloud yank username/myrepo/node packagecloud-1.0.1.tgz
```

Remove a scoped package called packagecloud-1.0.1.tgz from an npm registry named myrepo:

```
> package_cloud yank username/myrepo/node @computology/packagecloud-1.0.1.tgz
```

<a id="promote_pkg"></a>

### Promoting packages (Move a package)

You can move a package to a different epo by using the package\_cloud CLI:

```
> package_cloud promote username/myrepo/[distro/version] packagename.ext username/destination_repo
```

The packagename.ext must be the full filename of the package, including the extension.

Some packages (RPMs, Debs, Python packages, and JARs) are pushed to a specific distribution and version. When those packages are moved, the distribution/version must be specified and they will be moved to the same distribution/version in the destination repository.

Other package types (RubyGems and npm packages) can be moved without specifying a distribution or version, as these do not apply to RubyGem or npm packages.

Both repository owners and collaborators may move packages between repositories.

This operation is a move, not a copy, thus the source repository will no longer have a copy of the package when the operation has completed. Note that the download statistics
for the moved package will be cleared.

### Examples

Move a packaged called jake-1.0-2.src.rpm from a CentOS 6 repo name myrepo to repo2:

```
> package_cloud promote username/myrepo/el/6 jake-1.0-2.src.rpm username/repo2
```

Move a package called redis\_2.8.1-1\_amd64.deb from an Ubuntu Precise (12.04) repo named myrepo to repo2:

```
> package_cloud promote username/myrepo/ubuntu/precise redis_2.8.1-1_amd64.deb username/repo2
```

Move a package called packagecloud\_test-0.0.1.whl from a Python repo named myrepo to repo2:

```
> package_cloud promote username/myrepo/python packagecloud_test-0.0.1.whl username/repo2
```

Move a package called passenger-4.0.43.gem from a RubyGem repo named myrepo:

```
> package_cloud promote username/myrepo passenger-4.0.43.gem username/repo2
```

Move a package called packagecloud-1.0.1.tgz from an npm registry named myrepo:

```
> package_cloud promote username/myrepo/node packagecloud-1.0.1.tgz username/repo2
```

Move a scoped package called @computology/packagecloud-1.0.1.tgz from an npm registry named myrepo:

```
> package_cloud promote username/myrepo/node @computology/packagecloud-1.0.1.tgz username/repo2
```

<a id="install_repo"></a>

### Installing a repo

There are two methods you can use to install a repo:

1. You can visit the repo page and click the installation tab on the left side to get Bash scripts, a Chef cookbook, a Puppet module, and manual installation instructions.
2. You can also use the package\_cloud command line client. You will need to specify the type of repo you want installed on your system (deb, rpm, or gem). For example, to install a deb repo you would run:

   ```
   > package_cloud repository install username/reponame deb
   ```

<a id="os_distro_version"></a>

### OS versions for pushing and yanking packages

When pushing or yanking a package you can specify an OS and a version. If you do not specify one, the command line client will
walk you through choosing the correct OS and version.

The following table shows the OS and version strings that are valid for pushing and yanking:

### RubyGems

No OS or version is required. RubyGem packages may be pushed like this:

```
package_cloud push user/repo example-1.0.1.gem
```

### Node.js

npm packages may be pushed like this:

```
package_cloud push user/repo/node example-1.0.1.tgz
```

### Python

Python wheels, eggs, and source distributons can be pushed by specifying `python`. Python packages may be pushed like this:

```
package_cloud push user/repo/python example-1.0.1.whl
```

<a id="amazon-info"></a>

### Amazon Linux

Packages for Amazon Linux must use the string for [Enterprise Linux 6](#anchor-el) (el/6) when pushing, or yanking, from a packagecloud repository.

```
package_cloud push user/repo/el/6 amz-linux-package-1.0-2.el6.x86_64.rpm
```

```
package_cloud yank user/repo/el/6 amz-linux-package-1.0-2.el6.x86_64.rpm
```

<a id="anchor-elementaryos"></a>

### elementary OS

| Version | Push/Yank string |
| --- | --- |
| 0.1 jupiter | elementaryos/jupiter |
| 0.2 luna | elementaryos/luna |
| 0.3 freya | elementaryos/freya |
| 0.4 loki | elementaryos/loki |
| 5.0 juno | elementaryos/juno |
| 5.1 hera | elementaryos/hera |
| 6.0 odin | elementaryos/odin |
| 6.1 jolnir | elementaryos/jolnir |
| 7.0 horus | elementaryos/horus |
| 8.0 circe | elementaryos/circe |

*Example: pushing a package to 0.1 jupiter:*

```
package_cloud push user/repo/elementaryos/jupiter testpkg_1.0-2_amd64.deb
```

*Example: yanking a package from 0.1 jupiter:*

```
package_cloud yank user/repo/elementaryos/jupiter testpkg_1.0-2_amd64.deb
```

<a id="anchor-anyfile"></a>

### Anyfile

| Version | Push/Yank string |
| --- | --- |
| v1 | anyfile/1 |

*Example: pushing a package to v1:*

```
package_cloud push user/repo/anyfile/1 <package_name>
```

*Example: yanking a package from v1:*

```
package_cloud yank user/repo/anyfile/1 <package_name>
```

<a id="anchor-helm"></a>

### Helm

| Version | Push/Yank string |
| --- | --- |
| v1 | helm/v1 |

*Example: pushing a package to v1:*

```
package_cloud push user/repo/helm/v1 <package_name>
```

*Example: yanking a package from v1:*

```
package_cloud yank user/repo/helm/v1 <package_name>
```

<a id="anchor-amazon"></a>

### Amazon Linux

| Version | Push/Yank string |
| --- | --- |
| Amazon Linux 1 | amazon/1 |
| Amazon Linux 2 | amazon/2 |
| Amazon Linux 2023 | amazon/2023 |

*Example: pushing a package to Amazon Linux 1:*

```
package_cloud push user/repo/amazon/1 test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from Amazon Linux 1:*

```
package_cloud yank user/repo/amazon/1 test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-debian"></a>

### Debian

| Version | Push/Yank string |
| --- | --- |
| 4.0 etch | debian/etch |
| 5.0 lenny | debian/lenny |
| 6.0 squeeze | debian/squeeze |
| 7 wheezy | debian/wheezy |
| 8 jessie | debian/jessie |
| 9 stretch | debian/stretch |
| 10 buster | debian/buster |
| 11 bullseye | debian/bullseye |
| 12 bookworm | debian/bookworm |
| 13 Trixie | debian/trixie |
| 14 forky | debian/forky |
| 15 Duke | debian/duke |

*Example: pushing a package to 4.0 etch:*

```
package_cloud push user/repo/debian/etch testpkg_1.0-2_amd64.deb
```

*Example: yanking a package from 4.0 etch:*

```
package_cloud yank user/repo/debian/etch testpkg_1.0-2_amd64.deb
```

<a id="anchor-ubuntu"></a>

### Ubuntu

| Version | Push/Yank string |
| --- | --- |
| 4.10 Warty Warthog | ubuntu/warty |
| 5.04 Hoary Hedgehog | ubuntu/hoary |
| 5.10 Breezy Badger | ubuntu/breezy |
| 6.06 LTS Dapper Drake | ubuntu/dapper |
| 6.10 Edgy Eft | ubuntu/edgy |
| 7.04 Feisty Fawn | ubuntu/feisty |
| 7.10 Gutsy Gibbon | ubuntu/gutsy |
| 8.04 LTS Hardy Heron | ubuntu/hardy |
| 8.10 Intrepid Ibex | ubuntu/intrepid |
| 9.04 Jaunty Jackalope | ubuntu/jaunty |
| 9.10 Karmic Koala | ubuntu/karmic |
| 10.04 LTS Lucid Lynx | ubuntu/lucid |
| 10.10 Maverick Meerkat | ubuntu/maverick |
| 11.04 Natty Narwhal | ubuntu/natty |
| 11.10 Oneiric Ocelot | ubuntu/oneiric |
| 12.04 LTS Precise Pangolin | ubuntu/precise |
| 12.10 Quantal Quetzal | ubuntu/quantal |
| 13.04 Raring Ringtail | ubuntu/raring |
| 13.10 Saucy Salamander | ubuntu/saucy |
| 14.04 LTS Trusty Tahr | ubuntu/trusty |
| 14.10 Utopic Unicorn | ubuntu/utopic |
| 15.04 Vivid Vervet | ubuntu/vivid |
| 15.10 Wily Werewolf | ubuntu/wily |
| 16.04 LTS Xenial Xerus | ubuntu/xenial |
| 16.10 Yakkety Yak | ubuntu/yakkety |
| 17.04 Zesty Zapus | ubuntu/zesty |
| 17.10 Artful Aardvark | ubuntu/artful |
| 18.04 LTS Bionic Beaver | ubuntu/bionic |
| 18.10 Cosmic Cuttlefish | ubuntu/cosmic |
| 19.04 Disco Dingo | ubuntu/disco |
| 19.10 Eoan Ermine | ubuntu/eoan |
| 20.04 Focal Fossa | ubuntu/focal |
| 20.10 Groovy Gorilla | ubuntu/groovy |
| 21.04 Hirsute Hippo | ubuntu/hirsute |
| 21.10 Impish Indri | ubuntu/impish |
| 22.04 Jammy Jellyfish | ubuntu/jammy |
| 22.10 Kinetic Kudu | ubuntu/kinetic |
| 23.04 Lunar Lobster | ubuntu/lunar |
| 23.10 Mantic Minotaur | ubuntu/mantic |
| 24.04 LTS Noble Numbat | ubuntu/noble |
| 24.10 Oracular Oriole | ubuntu/oracular |
| 25.04 Plucky Puffin | ubuntu/plucky |
| 25.10 Questing Quokka | ubuntu/questing |
| 26.04 Resolute Raccoon | ubuntu/resolute |

*Example: pushing a package to 4.10 Warty Warthog:*

```
package_cloud push user/repo/ubuntu/warty testpkg_1.0-2_amd64.deb
```

*Example: yanking a package from 4.10 Warty Warthog:*

```
package_cloud yank user/repo/ubuntu/warty testpkg_1.0-2_amd64.deb
```

<a id="anchor-ol"></a>

### Oracle Linux

| Version | Push/Yank string |
| --- | --- |
| Oracle Linux 5.0 | ol/5 |
| Oracle Linux 6.0 | ol/6 |
| Oracle Linux 7.0 | ol/7 |
| Oracle Linux 8.0 | ol/8 |
| Oracle Linux 9.0 | ol/9 |
| Oracle Linux 10.0 | ol/10 |

*Example: pushing a package to Oracle Linux 10.0:*

```
package_cloud push user/repo/ol/10 test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from Oracle Linux 10.0:*

```
package_cloud yank user/repo/ol/10 test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-raspbian"></a>

### Raspbian

| Version | Push/Yank string |
| --- | --- |
| 7 wheezy | raspbian/wheezy |
| 8 jessie | raspbian/jessie |
| 9 stretch | raspbian/stretch |
| 10 buster | raspbian/buster |
| 11 bullseye | raspbian/bullseye |
| 12 bookworm | raspbian/bookworm |
| 13 trixie | raspbian/trixie |
| 14 forky | raspbian/forky |
| 15 duke | raspbian/duke |

*Example: pushing a package to 10 buster:*

```
package_cloud push user/repo/raspbian/buster testpkg_1.0-2_amd64.deb
```

*Example: yanking a package from 10 buster:*

```
package_cloud yank user/repo/raspbian/buster testpkg_1.0-2_amd64.deb
```

<a id="anchor-sles"></a>

### SUSE Linux Enterprise Server

| Version | Push/Yank string |
| --- | --- |
| SUSE Linux Enterprise Server 11.4 | sles/11.4 |
| SUSE Linux Enterprise Server 12 | sles/12.0 |
| SUSE Linux Enterprise Server 12.1 | sles/12.1 |
| SUSE Linux Enterprise Server 12.2 | sles/12.2 |
| SUSE Linux Enterprise Server 12.3 | sles/12.3 |
| SUSE Linux Enterprise Server 15.0 | sles/15.0 |
| SUSE Linux Enterprise Server 12.4 | sles/12.4 |
| SUSE Linux Enterprise Server 12.5 | sles/12.5 |
| SUSE Linux Enterprise Server 15.1 | sles/15.1 |
| SUSE Linux Enterprise Server 15.2 | sles/15.2 |
| SUSE Linux Enterprise Server 15.3 | sles/15.3 |
| SUSE Linux Enterprise Server 15.4 | sles/15.4 |
| SUSE Linux Enterprise Server 15.5 | sles/15.5 |
| SUSE Linux Enterprise Server 15.6 | sles/15.6 |
| SUSE Linux Enterprise Server 15.7 | sles/15.7 |
| SUSE Linux Enterprise Server 16.0 | sles/16.0 |

*Example: pushing a package to SUSE Linux Enterprise Server 11.4:*

```
package_cloud push user/repo/sles/11.4 test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from SUSE Linux Enterprise Server 11.4:*

```
package_cloud yank user/repo/sles/11.4 test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-opensuse"></a>

### openSUSE

| Version | Push/Yank string |
| --- | --- |
| openSUSE 13.1 | opensuse/13.1 |
| openSUSE 13.2 | opensuse/13.2 |
| openSUSE Leap 42.1 | opensuse/42.1 |
| openSUSE Leap 42.2 | opensuse/42.2 |
| openSUSE Leap 42.3 | opensuse/42.3 |
| openSUSE Leap 15.0 | opensuse/15.0 |
| openSUSE Leap 15.1 | opensuse/15.1 |
| openSUSE Leap 15.2 | opensuse/15.2 |
| openSUSE Leap 15.3 | opensuse/15.3 |
| openSUSE Leap 15.4 | opensuse/15.4 |
| openSUSE Leap 15.5 | opensuse/15.5 |
| openSUSE Leap 15.6 | opensuse/15.6 |
| openSUSE Leap 16.0 | opensuse/16.0 |

*Example: pushing a package to openSUSE 13.1:*

```
package_cloud push user/repo/opensuse/13.1 test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from openSUSE 13.1:*

```
package_cloud yank user/repo/opensuse/13.1 test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-fedora"></a>

### Fedora

| Version | Push/Yank string |
| --- | --- |
| 14 Laughlin | fedora/14 |
| 15 Lovelock | fedora/15 |
| 16 Verne | fedora/16 |
| 17 Beefy Miracle | fedora/17 |
| 18 Spherical Cow | fedora/18 |
| 19 Schrödinger's Cat | fedora/19 |
| 20 Heisenbug | fedora/20 |
| 21 Fedora 21 | fedora/21 |
| 22 Fedora 22 | fedora/22 |
| 23 Fedora 23 | fedora/23 |
| 24 Fedora 24 | fedora/24 |
| 25 Fedora 25 | fedora/25 |
| 26 Fedora 26 | fedora/26 |
| 27 Fedora 27 | fedora/27 |
| 28 Fedora 28 | fedora/28 |
| 29 Fedora 29 | fedora/29 |
| 30 Fedora 30 | fedora/30 |
| 31 Fedora 31 | fedora/31 |
| 32 Fedora 32 | fedora/32 |
| 33 Fedora 33 | fedora/33 |
| 34 Fedora 34 | fedora/34 |
| 35 Fedora 35 | fedora/35 |
| 36 Fedora 36 | fedora/36 |
| 37 Fedora 37 | fedora/37 |
| 38 Fedora 38 | fedora/38 |
| 39 Fedora 39 | fedora/39 |
| 40 Fedora 40 | fedora/40 |
| 41 Fedora 41 | fedora/41 |
| 42 Fedora 42 | fedora/42 |
| 43 Fedora 43 | fedora/43 |
| 44 Fedora 44 | fedora/44 |

*Example: pushing a package to 14 Laughlin:*

```
package_cloud push user/repo/fedora/14 test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from 14 Laughlin:*

```
package_cloud yank user/repo/fedora/14 test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-linuxmint"></a>

### LinuxMint

| Version | Push/Yank string |
| --- | --- |
| 16 petra | linuxmint/petra |
| 17 qiana | linuxmint/qiana |
| 17.1 rebecca | linuxmint/rebecca |
| 17.2 rafaela | linuxmint/rafaela |
| 17.3 rosa | linuxmint/rosa |
| 18 sarah | linuxmint/sarah |
| 18.1 serena | linuxmint/serena |
| 18.2 sonya | linuxmint/sonya |
| 18.3 sylvia | linuxmint/sylvia |
| 19 tara | linuxmint/tara |
| 19.1 tessa | linuxmint/tessa |
| 19.2 tina | linuxmint/tina |
| 19.3 tricia | linuxmint/tricia |
| 20 ulyana | linuxmint/ulyana |
| 20.1 ulyssa | linuxmint/ulyssa |
| 20.2 uma | linuxmint/uma |
| 20.3 una | linuxmint/una |
| 21 vanessa | linuxmint/vanessa |
| 21.1 vera | linuxmint/vera |
| 21.2 victoria | linuxmint/victoria |
| 21.3 virginia | linuxmint/virginia |
| 22 wilma | linuxmint/wilma |
| 22.1 xia | linuxmint/xia |

*Example: pushing a package to 16 petra:*

```
package_cloud push user/repo/linuxmint/petra testpkg_1.0-2_amd64.deb
```

*Example: yanking a package from 16 petra:*

```
package_cloud yank user/repo/linuxmint/petra testpkg_1.0-2_amd64.deb
```

<a id="anchor-java"></a>

### Java

| Version | Push/Yank string |
| --- | --- |
| Maven 2 | java/maven2 |

*Example: pushing a package to Maven 2:*

```
package_cloud push user/repo/java/maven2 <package_name>
```

*Example: yanking a package from Maven 2:*

```
package_cloud yank user/repo/java/maven2 <package_name>
```

<a id="anchor-poky"></a>

### poky (Yocto Project Reference Distribution)

| Version | Push/Yank string |
| --- | --- |
| 2.0 Jethro | poky/jethro |
| 2.1 Krogoth | poky/krogoth |
| 2.2 Morty | poky/morty |
| 2.3 Pyro | poky/pyro |
| 2.4 Rocko | poky/rocko |
| 2.5 Sumo | poky/sumo |
| 2.6 Thud | poky/thud |
| 2.7 Warrior | poky/warrior |
| 3.0 Zeus | poky/zeus |
| 3.1 Dunfell | poky/dunfell |
| 3.2 Gatesgarth | poky/gatesgarth |
| 3.3 Hardknott | poky/hardknott |
| 3.4 Honister | poky/honister |
| 4.0 Kirkstone | poky/kirkstone |
| 4.1 Langdale | poky/langdale |
| 4.2 Mickledore | poky/mickledore |
| 4.3 Nanbield | poky/nanbield |
| 5.0 Scarthgap | poky/scarthgap |
| 5.1 Styhead | poky/styhead |
| 5.2 Walnascar | poky/walnascar |
| 5.3 Whinlatter | poky/whinlatter |

*Example: pushing a package to 2.0 Jethro:*

```
package_cloud push user/repo/poky/jethro test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from 2.0 Jethro:*

```
package_cloud yank user/repo/poky/jethro test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-alpine"></a>

### Alpine Linux

| Version | Push/Yank string |
| --- | --- |
| 3.13 | alpine/v3.13 |
| 3.14 | alpine/v3.14 |
| 3.15 | alpine/v3.15 |
| 3.16 | alpine/v3.16 |
| 3.17 | alpine/v3.17 |
| 3.18 | alpine/v3.18 |
| 3.19 | alpine/v3.19 |
| 3.20 | alpine/v3.20 |
| 3.21 | alpine/v3.21 |
| 3.22 | alpine/v3.22 |
| 3.23 | alpine/v3.23 |

*Example: pushing a package to 3.13:*

```
package_cloud push user/repo/alpine/v3.13 test-0.7.4-r7.apk
```

*Example: yanking a package from 3.13:*

```
package_cloud yank user/repo/alpine/v3.13 test-0.7.4-r7.apk
```

<a id="anchor-el"></a>

### Enterprise Linux (CentOS, Red Hat, Amazon Linux)

| Version | Push/Yank string |
| --- | --- |
| Enterprise Linux 5.0 | el/5 |
| Enterprise Linux 6.0 / [Amazon Linux](#amazon-info) | el/6 |
| Enterprise Linux 7.0 | el/7 |
| Enterprise Linux 8.0 | el/8 |
| Enterprise Linux 9.0 | el/9 |
| Enterprise Linux 10.0 | el/10 |

*Example: pushing a package to Enterprise Linux 5.0:*

```
package_cloud push user/repo/el/5 test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from Enterprise Linux 5.0:*

```
package_cloud yank user/repo/el/5 test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-scientific"></a>

### Scientific Linux

| Version | Push/Yank string |
| --- | --- |
| Scientific Linux 5.0 | scientific/5 |
| Scientific Linux 6.0 | scientific/6 |
| Scientific Linux 7.0 | scientific/7 |

*Example: pushing a package to Scientific Linux 5.0:*

```
package_cloud push user/repo/scientific/5 test-1.0-2.el6.x86_64.rpm
```

*Example: yanking a package from Scientific Linux 5.0:*

```
package_cloud yank user/repo/scientific/5 test-1.0-2.el6.x86_64.rpm
```

<a id="anchor-huggingface"></a>

### Huggingface

| Version | Push/Yank string |
| --- | --- |
| models-v1 | huggingface/models-v1 |
| datasets-v1 | huggingface/datasets-v1 |
| spaces-v1 | huggingface/spaces-v1 |

*Example: pushing a package to datasets-v1:*

```
package_cloud push user/repo/huggingface/datasets-v1 <package_name>
```

*Example: yanking a package from datasets-v1:*

```
package_cloud yank user/repo/huggingface/datasets-v1 <package_name>
```

<a id="anchor-terraform"></a>

### Terraform

| Version | Push/Yank string |
| --- | --- |
| modules-v1 | terraform/modules-v1 |

*Example: pushing a package to modules-v1:*

```
package_cloud push user/repo/terraform/modules-v1 <package_name>
```

*Example: yanking a package from modules-v1:*

```
package_cloud yank user/repo/terraform/modules-v1 <package_name>
```

<a id="sso"></a>

## SSO

<a id="sso_requirements"></a>

### Requirements

---

### In your identity management service

To implement SSO login with packagecloud, customers must create a new application in their identity management service (Okta, Google Admin etc.), with the following details:

1. #### ACS URL:

   ```
   https://dev-px9pgfj4.us.auth0.com/login/callback?connection={email_domain}
   ```

   *Example: If the email domain is `packagecloud.io`, the URL should be: `https://dev-px9pgfj4.us.auth0.com/login/callback?connection=packagecloudio` (without '.')*
2. #### Entity ID:

   ```
   urn:auth0:dev-px9pgfj4:{email_domain_no_special_chars}
   ```

   *Example: `urn:auth0:dev-px9pgfj4:packagecloudio` (without '.')*
3. #### Add mapping attribute:

   Please map your `email` attribute to an app attribute called `email`.

   In some cases the default email field has a prefix, so we are normalizing it. For instance: `primary_email` → `email`

### Update packagecloud admins

**To enable SSO-login to packagecloud, please send these details to our team member you are in contact with, or [support@packagecloud.io](mailto: support@packagecloud.io):**

1. Your application's SSO URL,
2. Your application's x509 certificate file,
3. The SSO login-enabled person's/people's email (used to register with packagecloud),
4. Whether the user is an SSO admin (if applicable)

We appreciate your patience whilst our admins confirm the details and update the user's account.

<a id="okta"></a>

### Okta

---

### Okta Configuration

The following steps should be completed by an Admin user of your Okta account in the Admin UI.

### Settings for creating a new SAML 2.0 Application

- **Single sign on URL**

  ```
  https://dev-px9pgfj4.us.auth0.com/login/callback?connection={email_domain}
  ```

  *Example: If the email domain is `packagecloud.io`, the URL should be: `https://dev-px9pgfj4.us.auth0.com/login/callback?connection=packagecloudio`* (without '.')
- **Entity ID**

  ```
  urn:auth0:dev-px9pgfj4:{email_domain_no_special_chars}
  ```

  *Example: `urn:auth0:dev-px9pgfj4:packagecloudio` (without '.')*
- **Name ID format:** `Unspecified`
- **Application username:** `Email`
- **Attribute Statements:**

  - Name: `email`
  - Name format: `Unspecified`
  - Value: `user.email`

### Add/assign new users to the account

1. **Create a new Person**

   In Directory (side nav) → People: Click the 'Add Person' button, enter the details, check the 'Send user activation email now' box and Save.

   NOTE: The inputted email should match the email used to register their packagecloud account.

   They will receive an email with prompts to create an account in Okta, and their Status will remain as 'Pending user action' until complete.
2. **Assign the user to the application**

   When the new user's Status is confirmed 'Active', go to your Application's Assignments (Applications (side nav) → Applications → <your\_app\_name> → Assignments), click the 'Assign' button, and 'Assign to People' from the dropdown menu.

   Select the user, click 'Assign' next to their name.

   Confirm the correct User Name, which should be the email used to register their packagecloud account, click 'Save and Go Back'.

### Update packagecloud admins

**To enable SSO-login to packagecloud, please send these details to our team member you are in contact with, or [support@packagecloud.io](mailto: support@packagecloud.io):**

1. Your application's Identity Provider Single Sign-On URL,
2. Your application's x509 certificate file,
3. The SSO login-enabled person's/people's email (used to register with packagecloud),
4. Whether the user is an SSO admin (if applicable)

The first two can be confirmed in the Okta Admin UI under Applications (side nav) → Applications → <your\_app\_name> → Sign On → View Setup Instructions

We appreciate your patience whilst our admins confirm the details and update the user's account.

## Billing & Pricing

<a id="pricing"></a>

Please refer to our [Billing & Pricing FAQ](https://packagecloud.io/pricing/faq) for detailed info.

<a id="troubleshooting"></a>

## Troubleshooting

<a id="package_not_found"></a>

### Package not found

There are two main reasons why this can happen: there are [unavailable packages](#no_available_packages) suitable for your system, OR your system contains [stale cached package metadata.](#stale_cached_metadata)

<a id="no_available_packages"></a>1. **No available packages suitable for your system**

This happens because there is a mismatch between the attributes of the available packages and the attributes of the system that is trying to install those packages. Four of the most common mismatches are as follows:

**In these first two cases, we recommend to contact the respository owner directly for further support:**

- **No packages for the architecture:** For example, only packages with the architecture 'amd64' is available in the repository, but the system has the architecture 'i386'.
- **Unavailable package format:** For example, there are only RPM packages in the repository but the client system uses the DEB package format.

**These two cases can *potentially* be resolved by [forcing the os/dist](#force_os_dist_package_not_found) when running the repository installation script to generate repo config files for a distribution or version, which the package you intend to install is available for, and that distribution or version is also compatible to the system:**

- **Unavailable distribution:** For example, only Ubuntu packages are available in the repository, but the client system is running LinuxMint.
- **Distribution version mismatch:** For example, only Ubuntu/Precise packages are available in the repository, but the client system is running Ubuntu/Jammy.
<a id="force_os_dist_package_not_found"></a>

#### Forcing the os/dist when installing the repository:

The following steps refer to Debian packages, but the general process can be applied for other package types (like RPM) too.

*For example: I am running an Ubuntu/Jammy machine and I wish to install a Debian test package from the [packagecloud-test-packages repository](https://packagecloud.io/Computology/packagecloud-test-packages).*

1. **Double check the repository to confirm the available os/dist**

Currently the [packagecloud-test-packages repository](https://packagecloud.io/Computology/packagecloud-test-packages) has a Debian package uploaded only for `Ubuntu/Precise` NOT `Ubuntu/Jammy`.

2. **Download the installation script**

The repository installation script command can be found by clicking on the package in the repository, e.g., [packagecloud-test-package for `Ubuntu/Precise`](https://packagecloud.io/Computology/packagecloud-test-packages/packages/ubuntu/precise/packagecloud-test_1.1-2_amd64.deb). Depending on the package type, it may differ from the below.

```
curl -s https://packagecloud.io/install/repositories/Computology/packagecloud-test-packages/script.deb.sh > script.sh
```

3. **Make the script executable**

```
chmod 755 script.sh
```

4. **Specify a supported os/dist when running the script to force the repository installation**

As the Debian package I wish to install has only been uploaded for `Ubuntu/Precise`, I will set them as the os and dist variables prior to running the script.

```
os=ubuntu dist=precise ./script.sh
```

5. **Running the installation command will then install the available package for the specified version**

```
sudo apt-get install packagecloud-test=1.1-2
```

<a id="stale_cached_metadata"></a>2. **Stale cached package metadata on your system**

- **APT**

You can update it by running:

```
sudo apt-get clean && sudo apt-get update
```

- **YUM**

You can refresh it by running

```
sudo yum clean all && sudo yum update
```

You can also set

```
metadata_expires=[time in seconds]
```

in your repository config (found in /etc/yum/yum.repos.d/) to smaller value to allow for YUM to automatically refresh
the metadata. See the man page (man 5 yum.conf) for more information.

<a id="unable_to_download_repo_config"></a>

### Unable to download repo config

You may encounter this error when attempting to run the repository installation script:

```
Unable to download repo config from: https://packagecloud.io/install/repositories/username/reponame/config_file.list?o
s=OS&dist=DIST&source=script

This usually happens if your operating system is not supported by
packagecloud.io, or this script's OS detection failed.

You can override the OS detection by setting os= and dist= prior to running this script.
You can find a list of supported OSes and distributions on our website: https://packagecloud.io/docs#os_distro_version

For example, to force Ubuntu Trusty: os=ubuntu dist=trusty ./script.sh
```

This error typically means Packagecloud currently does not know how to create the repo config for your system. Perhaps you are using a [supported OS](#os_distro_version) but with a newly released version that we are in the process of implementing. Or, you may be running an OS/dist which Packagecloud does not yet automatically detect.

<a id="force_os_dist_repo_config"></a>

#### How to resolve this:

The following steps refer to Debian packages, but the general process can be applied for other package types (like RPM) too.

*For example: Hypothetically if Packagecloud had not yet added support for `Debian/Bullseye` running on my machine and I wish to install the [packagecloud-test-packages repository](https://packagecloud.io/Computology/packagecloud-test-packages).*

1. **Download the installation script**

The repository installation script command can be found by clicking on the package in the repository, e.g., [packagecloud-test-package for `Ubuntu/Precise`](https://packagecloud.io/Computology/packagecloud-test-packages/packages/ubuntu/precise/packagecloud-test_1.1-2_amd64.deb). Depending on the package type, it may differ from the below.

```
curl -s https://packagecloud.io/install/repositories/Computology/packagecloud-test-packages/script.deb.sh > script.sh
```

2. **Make the script executable**

```
chmod 755 script.sh
```

3. **Specify a supported os/dist to force the installation when running the script**

I can set the `os` and `dist` variables to a Packagecloud supported os/dist as similar as possible to my system. To avoid future potential ['package not found' errors](#package_not_found), I have set it to match the os/dist of an available package in the repository (Ubuntu/Precise).

```
os=ubuntu dist=precise ./script.sh
```

<a id="gdpr"></a>

### GDPR

The General Data Protection Regulation (GDPR) is a new European data protection regulation
adopted by the EU Commission, which aims to strengthen the security of personal data.

Below is some information about the steps Packagecloud is taking to meet the GDPR
requirements, and how we are working with our EU customers to help them meet their
compliance obligations.

<a id="controller_processor"></a>

### Is Packagecloud a data controller or data processor?

In general, Packagecloud is a data controller for personal data derived on its website, and
personal information such as contact information collected directly from our EU customers.

Packagecloud is a data processor when its EU customers collect the personal information of
their employees or customers and upload that personal data to their Packagecloud account. In
this case, the EU customer is the data controller for that personal information.

<a id="customer_controller"></a>

### What are customers’ responsibilities as a data controller?

EU customers who have collected the personal information of their employees or customers
need to ensure that they have legal consent of those parties under the GDPR, and that there is
an adequate level of protection for that data exported out of the EU.

<a id="customer_dpa"></a>

### Does Packagecloud have a Customer DPA?

Yes, it does. Contact us at [support@packagecloud.io](mailto:support@packagecloud.io)
and it will be provided to you. Also Packagecloud enters into standard contractual clauses with EU
customers upon request.
