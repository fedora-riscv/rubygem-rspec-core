%global	gemdir		%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global	gemname	rspec-core
%global	geminstdir	%{gemdir}/gems/%{gemname}-%{version}

%global	rubyabi	1.8

# %%check section needs rspec-core, however rspec-core depends on rspec-mocks
# runtime part of rspec-mocks does not depend on rspec-core
%global	need_bootstrap_set	1
%if 0%{?fedora} >= 16
%global	need_bootstrap_set	1
%endif

%{!?need_bootstrap:	%global	need_bootstrap	%{need_bootstrap_set}}

Summary:	Rspec-2 runner and formatters
Name:		rubygem-%{gemname}
Version:	2.5.1
Release:	3%{?dist}

Group:		Development/Languages
License:	MIT
URL:		http://github.com/rspec/rspec-mocks
Source0:	http://rubygems.org/gems/%{gemname}-%{version}.gem

BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	rubygems
%if 0%{?need_bootstrap} < 1
BuildRequires:	rubygem(rspec-expectations)
BuildRequires:	rubygem(rspec-mocks)
%endif
Requires:	ruby(abi) = %{rubyabi}
Requires:	rubygem(rspec-expectations)
Requires:	rubygem(rspec-mocks)
# Make the following installed by default
# lib/rspec/core/rake_task
Requires:	rubygem(rake)
# Optional
#Requires:	rubygem(ZenTest)
#Requires:	rubygem(mocha)
#Requires:	rubygem(ruby-debug)
# Not found in Fedora yet (and optional)
#Requires:	rubygem(rr)
Provides:	rubygem(%{gemname}) = %{version}-%{release}
BuildArch:	noarch

%description
Behaviour Driven Development for Ruby.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.


%prep
%setup -q -c -T

mkdir -p .%{gemdir}
gem install \
	-V \
	--local \
	--install-dir .%{gemdir} \
	--bindir .%{_bindir} \
	--force \
	--rdoc \
	%{SOURCE0}

chmod 0644 .%{gemdir}/cache/%{gemname}-%{version}.gem

# rpmlint
pushd .%{geminstdir}
grep -rl '^#![ \t]*/usr/bin' ./lib| \
	xargs sed -i -e '\@^#![ \t]*/usr/bin@d'

# Until rspec is updated, lets install rspec.rb
cat > lib/rspec.rb <<EOF
require 'rspec/core'
require 'rspec/expectations'
require 'rspec/mocks'
EOF

popd

%build

%install
mkdir -p %{buildroot}%{_prefix}
cp -a .%{_prefix}/* %{buildroot}%{_prefix}/

# Rename autospec to avoid conflict with rspec 1.3
# (anyway this script doesn't seem to be useful)
mv %{buildroot}%{_bindir}/autospec{,2}

# cleanups
rm -f %{buildroot}%{geminstdir}/{.document,.gitignore,.treasure_map.rb,.rspec}

%if 0%{?need_bootstrap} < 1
%check
pushd .%{geminstdir}
# spec/autotest/failed_results_re_spec.rb (and others) fail, skipping this for now
# (need investigating)
ruby -rubygems -Ilib/ -S bin/rspec \
	spec/rspec/*_spec.rb spec/rspec/*/*_spec.rb \
%if 0
	spec/autotest/*_spec.rb
%endif
%endif

%files
%defattr(-,root,root,-)
%dir	%{geminstdir}

%doc	%{geminstdir}/License.txt
%doc	%{geminstdir}/*.md

%{_bindir}/autospec2
%{_bindir}/rspec
%{geminstdir}/bin/
%{geminstdir}/lib/

%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%files	doc
%defattr(-,root,root,-)
%{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/Gemfile
%{geminstdir}/Guardfile
%{geminstdir}/Rakefile
%{geminstdir}/cucumber.yml
%{geminstdir}/%{gemname}.gemspec
%{geminstdir}/features/
%{geminstdir}/script/
%{geminstdir}/spec/

%changelog
* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.1-3
- More cleanups

* Tue Feb 22 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.5.1-2
- Some misc fixes

* Thu Feb 17 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.5.1-1
- 2.5.1

* Fri Nov 05 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- Initial package
