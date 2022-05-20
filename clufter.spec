%{?python_enable_dependency_generator}
# virtual provides:
#   clufter        -> clufter-cli
#   clufter-lib    -> python.+-clufter (any if multiple)


# https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:           clufter
Version:        0.77.2
Release:        3
Summary:        Tool/library for transforming/analyzing cluster configuration formats
License:        GPLv2+
URL:            https://pagure.io/%{name}

BuildRequires:  gcc
# required for autosetup macro
BuildRequires:  git-core
%if 0%{defined gpgverify}
# required for OpenPGP package signature verification (per guidelines)
BuildRequires: gnupg2
%endif

# Python 3 related
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-lxml
BuildRequires:  python3-distro

# following to ensure "which bash" (and, in extension, "which sh") works
BuildRequires:  bash which

BuildRequires:  pkgconfig(libxml-2.0)

# schemadir path pointer (former since pacemaker 2.0.3)
%if 0%{?fedora} >= 32
BuildRequires:  pkgconfig(pacemaker-schemas)
%else
BuildRequires:  pkgconfig(pacemaker-cib)
%endif
# nschemas themselves (former since pacemaker 2.0.1)
%if 0%{?fedora} >= 30
BuildRequires:  pacemaker-schemas
%else
BuildRequires:  pacemaker
%endif

# needed to squash multi-file schemas to single file
BuildRequires:  jing
# needed for xsltproc and xmllint respectively
BuildRequires:  libxslt libxml2

#global test_version
%global testver      %{?test_version}%{?!test_version:%{version}}

Source0:        https://releases.pagure.org/%{name}/%{name}-%{version}.tar.gz
Source1:        https://releases.pagure.org/%{name}/%{name}-%{testver}-tests.tar.xz
Source2:        https://pagure.io/%{name}/raw/v%{version}/f/misc/fix-jing-simplified-rng.xsl
#Source3:       https://pagure.io/#{name}/raw/v#{version}/f/misc/pacemaker-borrow-schemas
Source3:        https://pagure.io/%{name}/raw/50377b47601b88381537fa13ab466fe2cb37c56a/f/misc/pacemaker-borrow-schemas
%if 0%{defined gpgverify}
Source4:        https://releases.pagure.org/%{name}/%{name}-%{version}.tar.gz.asc
# publicly stated signature key rollover policy:
# https://lists.clusterlabs.org/pipermail/users/2019-August/026234.html
Source5:        https://releases.pagure.org/%{name}/%{name}-2019-08-15-5CD7F9EF.keyring
%endif

#Patch0:        https://pagure.io/clufter/c/b83e3091a7febd715cc0502dc154e43edb2d44f1.patch#/compat-Python-3.9-no-longer-offers-collections.Mutable-ABCs.patch
#Patch1:        https://pagure.io/clufter/c/2b1b834972a8834410d9e0c348c9aeda07c010af.patch#/compat-Python-3.9-no-longer-raises-ValueError-at-some-bound.patch
#Patch2:        https://pagure.io/clufter/c/7f4125ceefaf1dd1fb66bf96509c4b0acf2d5e94.patch#/plugin_registry-fix-a-problem-with-native-plugins-missing.patch
Patch0:         compat-Python-3.9-no-longer-offers-collections.Mutable-ABCs.patch
Patch1:         compat-Python-3.9-no-longer-raises-ValueError-at-some-bound.patch
Patch2:         plugin_registry-fix-a-problem-with-native-plugins-missing.patch
%description
While primarily aimed at (CMAN,rgmanager)->(Corosync/CMAN,Pacemaker) cluster
stacks configuration conversion (as per RHEL trend), the command-filter-format
framework (capable of XSLT) offers also other uses through its plugin library.

%package cli
Summary:        Tool for transforming/analyzing cluster configuration formats
Provides:       %{name} = %{version}-%{release}

BuildRequires:  bash-completion

BuildRequires:  help2man

# following for pkg_resources module
Requires:       python3-setuptools
Requires:       python3-%{name} = %{version}-%{release}
Requires:       %{_bindir}/nano
BuildArch:      noarch

%description cli
While primarily aimed at (CMAN,rgmanager)->(Corosync/CMAN,Pacemaker) cluster
stacks configuration conversion (as per RHEL trend), the command-filter-format
framework (capable of XSLT) offers also other uses through its plugin library.

This package contains %{name} command-line interface for the underlying
library (packaged as python3-%{name}).

%package -n python3-%{name}
Summary:        Library for transforming/analyzing cluster configuration formats
License:        GPLv2+ and GFDL

Provides:       %{name}-lib = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}
Obsoletes:      python-%{name} < %{version}-%{release}
Obsoletes:      python2-%{name} < %{version}-%{release}
Requires:       %{name}-bin = %{version}-%{release}
BuildArch:      noarch

%description -n python3-%{name}
While primarily aimed at (CMAN,rgmanager)->(Corosync/CMAN,Pacemaker) cluster
stacks configuration conversion (as per RHEL trend), the command-filter-format
framework (capable of XSLT) offers also other uses through its plugin library.

This package contains %{name} library including built-in plugins.

%package bin
Summary:        Common internal compiled files for %{name}
License:        GPLv2+

Requires:       %{name}-common = %{version}-%{release}

%description bin
While primarily aimed at (CMAN,rgmanager)->(Corosync/CMAN,Pacemaker) cluster
stacks configuration conversion (as per RHEL trend), the command-filter-format
framework (capable of XSLT) offers also other uses through its plugin library.

This package contains internal, arch-specific files for %{name}.

%package common
Summary:        Common internal data files for %{name}
License:        GPLv2+
BuildArch:      noarch

%description common
While primarily aimed at (CMAN,rgmanager)->(Corosync/CMAN,Pacemaker) cluster
stacks configuration conversion (as per RHEL trend), the command-filter-format
framework (capable of XSLT) offers also other uses through its plugin library.

This package contains internal, arch-agnostic files for %{name}.

%package lib-general
Summary:        Extra %{name} plugins usable for/as generic/auxiliary products
Requires:       %{name}-lib = %{version}-%{release}
BuildArch:      noarch

%description lib-general
This package contains set of additional plugins targeting variety of generic
formats often serving as a byproducts in the intermediate steps of the overall
process arrangement: either experimental commands or internally unused,
reusable formats and filters.

%package lib-ccs
Summary:        Extra plugins for transforming/analyzing CMAN configuration
Requires:       %{name}-lib-general = %{version}-%{release}
BuildArch:      noarch

%description lib-ccs
This package contains set of additional plugins targeting CMAN cluster
configuration: either experimental commands or internally unused, reusable
formats and filters.

%package lib-pcs
Summary:        Extra plugins for transforming/analyzing Pacemaker configuration
Requires:       %{name}-lib-general = %{version}-%{release}
BuildArch:      noarch

%description lib-pcs
This package contains set of additional plugins targeting Pacemaker cluster
configuration: either experimental commands or internally unused, reusable
formats and filters.

%prep
%if 0%{defined gpgverify}
%{gpgverify} --keyring='%{SOURCE5}' --signature='%{SOURCE4}' --data='%{SOURCE0}'
%endif
%setup -b1 -q
pushd clufter
%global __scm git_am
%__scm_setup_git
%autopatch -p1
popd

%if "%{testver}" != "%{version}"
    %{__cp} -a ../"%{name}-%{testver}"/* .
%endif

## for some esoteric reason, the line above has to be empty
%{__python3} setup.py saveopts -f setup.cfg pkg_prepare \
                      --ccs-flatten='%{_libexecdir}/%{name}-%{version}/ccs_flatten' \
                      --editor='%{_bindir}/nano' \
                      --extplugins-shared='%{_datarootdir}/%{name}/ext-plugins' \
                      --ra-metadata-dir='%{_datadir}/cluster' \
                      --ra-metadata-ext='metadata' \
                      --shell-posix='%(which sh 2>/dev/null || echo /bin/SHELL-POSIX)' \
                      --shell-bashlike='%(which bash 2>/dev/null || echo /bin/SHELL-BASHLIKE)'
%{__python3} setup.py saveopts -f setup.cfg pkg_prepare \
  --report-bugs='https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora&component=%{name}'

%build
# see https://fedoraproject.org/wiki/Changes/python3_c.utf-8_locale;
# specifically:
#   File "setup.py", line 466, in _pkg_prepare_file
#     content = fr.read()
#   File "/usr/lib64/python3.5/encodings/ascii.py", line 26, in decode
#     return codecs.ascii_decode(input, self.errors)[0]
# UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 221: ordinal not in range(128)
export LC_ALL=C.UTF-8 LANG=C.UTF-8
%py3_build

%{__python3} -I ./run-dev --skip-ext --completion-bash 2>/dev/null \
  | sed 's|run[-_]dev|%{name}|g' > .bashcomp
# generate man pages (proper commands and aliases from a sorted sequence)
%{__mkdir_p} -- .manpages/man1
{ echo; %{__python3} -I ./run-dev -l | sed -n 's|^  \(\S\+\).*|\1|p' \
  | sort; } > .subcmds
sed -e 's:\(.\+\):\\\&\\fIrun_dev-\1\\fR\\\|(1), :' \
  -e '1s|\(.*\)|\[SEE ALSO\]\n|' \
  -e '$s|\(.*\)|\1\nand perhaps more|' \
  .subcmds > .see-also
help2man -N -h -H -i .see-also \
  -n "$(sed -n '2s|[^(]\+(\([^)]\+\))|\1|p' README)" \
  '%{__python3} -I ./run-dev' | sed 's|run\\\?[-_]dev|%{name}|g' \
  > ".manpages/man1/%{name}.1"
while read cmd; do
  [ -n "${cmd}" ] || continue
  echo -e "#\!/bin/sh\n{ [ \$# -ge 1 ] && [ \"\$1\" = \"--version\" ] \
  && %{__python3} -I ./run-dev \"\$@\" \
  || %{__python3} -I ./run-dev \"${cmd}\" \"\$@\"; }" > ".tmp-${cmd}"
  chmod +x ".tmp-${cmd}"
  grep -v "^${cmd}\$" .subcmds \
    | grep -e '^$' -e "$(echo ${cmd} | cut -d- -f1)\(-\|\$\)" \
    | sed -e 's:\(.\+\):\\\&\\fIrun_dev-\1\\fR\\\|(1), :' \
      -e '1s|\(.*\)|\[SEE ALSO\]\n\\\&\\fIrun_dev\\fR\\\|(1), \n|' \
      -e '$s|\(.*\)|\1\nand perhaps more|' > .see-also
  # XXX uses ";;&" bashism
  case "${cmd}" in
  ccs[2-]*)
    sed -i \
      '1s:\(.*\):\1\n\\\&\\fIcluster.conf\\fR\\\|(5), \\\&\\fIccs\\fR\\\|(7), :' \
    .see-also
    ;;&
  ccs2pcs*)
    sed -i \
      '1s:\(.*\):\1\n\\\&\\fI%{_defaultdocdir}/%{name}-%{version}/rgmanager-pacemaker\\fR\\\|, :' \
    .see-also
    ;;&
  *[2-]pcscmd*)
    sed -i '1s:\(.*\):\1\n\\\&\\fIpcs\\fR\\\|(8), :' .see-also
    ;;&
  esac
  help2man -N -h -H -i .see-also -n "${cmd}" "./.tmp-${cmd}" \
    | sed 's|run\\\?[-_]dev|%{name}|g' \
  > ".manpages/man1/%{name}-${cmd}.1"
done < .subcmds

OUTPUTDIR=.schemas POSTPROCESS="%{SOURCE2}" sh "%{SOURCE3}" --clobber

%install
# see build section
export LC_ALL=C.UTF-8 LANG=C.UTF-8
%py3_install

# following is needed due to umask 022 not taking effect(?) leading to 775
%{__chmod} -- g-w '%{buildroot}%{_libexecdir}/%{name}-%{version}/ccs_flatten'
# %%{_bindir}/%%{name} should have been created
test -f '%{buildroot}%{_bindir}/%{name}' \
  || %{__install} -D -pm 644 -- '%{buildroot}%{_bindir}/%{name}' \
                                '%{buildroot}%{_bindir}/%{name}'

# move data files from python-specific locations to a single common one
# and possibly symlink that back
%{__mkdir_p} -- '%{buildroot}%{_datarootdir}/%{name}/formats'
for format in cib corosync; do
  %{__cp} -a -t '%{buildroot}%{_datarootdir}/%{name}/formats' \
          -- "%{buildroot}%{python3_sitelib}/%{name}/formats/${format}"

  %{__rm} -f -- "%{buildroot}%{python3_sitelib}/%{name}/formats/${format}"/*
  ln -s -t "%{buildroot}%{python3_sitelib}/%{name}/formats/${format}" \
     -- $(pushd "%{buildroot}%{_datarootdir}/%{name}/formats/${format}" >/dev/null; \
          ls -1A | sed "s:.*:%{_datarootdir}/%{name}/formats/${format}/\\0:")
done

# move ext-plugins from python-specific locations to a single common one
# incl. the different sorts of precompiled bytecodes
%{__mkdir_p} -- '%{buildroot}%{_datarootdir}/%{name}/ext-plugins'
%{__cp} -af -t '%{buildroot}%{_datarootdir}/%{name}/ext-plugins' \
        -- '%{buildroot}%{python3_sitelib}/%{name}'/ext-plugins/*
%{__rm} -rf -- '%{buildroot}%{python3_sitelib}/%{name}'/ext-plugins/*/


declare bashcompdir="$(pkg-config --variable=completionsdir bash-completion \
                       || echo '%{_datadir}/bash-completion/completions')"
declare bashcomp="${bashcompdir}/%{name}"
%{__install} -D -pm 644 -- \
  .bashcomp '%{buildroot}%{_sysconfdir}/%{name}/bash-completion'
%{__mkdir_p} -- "%{buildroot}${bashcompdir}"
ln -s '%{_sysconfdir}/%{name}/bash-completion' "%{buildroot}${bashcomp}"
# own %%{_datadir}/bash-completion in case of ...bash-completion/completions,
# more generally any path up to any of /, /usr, /usr/share, /etc
while true; do
  test "$(dirname "${bashcompdir}")" != "/" \
  && test "$(dirname "${bashcompdir}")" != "%{_prefix}" \
  && test "$(dirname "${bashcompdir}")" != "%{_datadir}" \
  && test "$(dirname "${bashcompdir}")" != "%{_sysconfdir}" \
  || break
  bashcompdir="$(dirname "${bashcompdir}")"
done
cat >.bashcomp-files <<-EOF
	${bashcompdir}
	%dir %{_sysconfdir}/%{name}
	%verify(not size md5 mtime) %{_sysconfdir}/%{name}/bash-completion
EOF
%{__mkdir_p} -- '%{buildroot}%{_mandir}'
%{__cp} -a -t '%{buildroot}%{_mandir}' -- .manpages/*
%{__cp} -a -f -t '%{buildroot}%{_datarootdir}/%{name}/formats/cib' \
              -- .schemas/pacemaker-*.*.rng
%{__mkdir_p} -- '%{buildroot}%{_defaultdocdir}/%{name}-%{version}'
%{__cp} -a -t '%{buildroot}%{_defaultdocdir}/%{name}-%{version}' \
           -- gpl-2.0.txt doc/*.txt doc/rgmanager-pacemaker

%check
# just a basic sanity check
# we need to massage RA metadata files and PATH so the local run works
# XXX we could also inject buildroot's site_packages dir to PYTHONPATH
declare ret=0 \
        ccs_flatten_dir="$(dirname '%{buildroot}%{_libexecdir}/%{name}-%{version}/ccs_flatten')"
ln -s '%{buildroot}%{_datadir}/cluster'/*.'metadata' \
      "${ccs_flatten_dir}"
# see build section
export LC_ALL=C.UTF-8 LANG=C.UTF-8
PATH="${PATH:+${PATH}:}${ccs_flatten_dir}" PYTHONEXEC="%{__python3} -I" ./run-tests
ret=$?
%{__rm} -f -- "${ccs_flatten_dir}"/*.'metadata'
[ ${ret} -eq 0 ] || exit ${ret}

%post cli
if [ $1 -gt 1 ]; then  # no gain regenerating it w/ fresh install (same result)
declare bashcomp="%{_sysconfdir}/%{name}/bash-completion"
%{_bindir}/%{name} --completion-bash > "${bashcomp}" 2>/dev/null || :
fi

%post lib-general
declare bashcomp="%{_sysconfdir}/%{name}/bash-completion"
# if the completion file is not present, suppose it is not desired
test -x '%{_bindir}/%{name}' && test -f "${bashcomp}" \
  && %{_bindir}/%{name} --completion-bash > "${bashcomp}" 2>/dev/null || :

%post lib-ccs
declare bashcomp="%{_sysconfdir}/%{name}/bash-completion"
# if the completion file is not present, suppose it is not desired
test -x '%{_bindir}/%{name}' && test -f "${bashcomp}" \
  && %{_bindir}/%{name} --completion-bash > "${bashcomp}" 2>/dev/null || :

%post lib-pcs
declare bashcomp="%{_sysconfdir}/%{name}/bash-completion"
# if the completion file is not present, suppose it is not desired
test -x '%{_bindir}/%{name}' && test -f "${bashcomp}" \
  && %{_bindir}/%{name} --completion-bash > "${bashcomp}" 2>/dev/null || :

%files cli -f .bashcomp-files
%{_mandir}/man1/*.1*
%{_bindir}/%{name}

%files -n python3-%{name}
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-*.egg-info

%files bin
%{_libexecdir}/%{name}-%{version}

%files common
%{_datadir}/cluster
%{_datarootdir}/%{name}
%dir %{_defaultdocdir}/%{name}-%{version}
%{_defaultdocdir}/%{name}-%{version}/*[^[:digit:]]
%license %{_defaultdocdir}/%{name}-%{version}/*[[:digit:]].txt

%files lib-general
%{_datarootdir}/%{name}/ext-plugins/lib-general

%files lib-ccs
%{_datarootdir}/%{name}/ext-plugins/lib-ccs

%files lib-pcs
%{_datarootdir}/%{name}/ext-plugins/lib-pcs

%changelog
* Fri May 20 2022 caodongxia <caodongxia@h-partners.com> - 0.77.2-3
- remove useless code

* Tue Feb 23 2021 yangzhao <yangzhao1@kylinos.cn> - 0.77.2-2
- remove python2 support

* Fri Dec 4 2020 liqiuyu <liqiuyu@kylinos.cn> - 0.77.2-1
- Init python-clufter project
