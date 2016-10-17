%{?scl:%scl_package concurrentlinkedhashmap-lru}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}concurrentlinkedhashmap-lru
Version:	1.4.2
Release:	5%{?dist}
Summary:	A ConcurrentLinkedHashMap for Java
License:	ASL 2.0
Url:		https://github.com/ben-manes/concurrentlinkedhashmap
Source0:	https://github.com/ben-manes/concurrentlinkedhashmap/archive/%{pkg_name}-%{version}.tar.gz

# test deps
%if 0
BuildRequires:	mvn(com.github.stephenc.high-scale-lib:high-scale-lib)
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(commons-lang:commons-lang)
BuildRequires:	mvn(net.sf.ehcache:ehcache)
BuildRequires:	mvn(org.hamcrest:hamcrest-library) >= 1.3
BuildRequires:	mvn(org.mockito:mockito-all)
BuildRequires:	mvn(org.testng:testng)
# unavailable test deps
BuildRequires:	mvn(com.google.caliper:caliper)
BuildRequires:	mvn(com.jayway.awaitility:awaitility)
# require cache-benchmark == r7903 from http://sourceforge.net/projects/cachebenchfwk/
BuildRequires: mvn(org.cachebench:cache-benchmark)
%endif

BuildRequires: %{?scl_prefix_maven}maven-local
BuildRequires: %{?scl_prefix_maven}maven-plugin-bundle
BuildRequires: %{?scl_prefix_maven}maven-site-plugin
BuildRequires: %{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires: %{?scl_prefix_maven}mvn(com.google.code.findbugs:jsr305)
%{?scl:Requires: %scl_runtime}

BuildArch:     noarch

%description
A high performance version of java.util.LinkedHashMap
for use as a software cache.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n concurrentlinkedhashmap-%{pkg_name}-%{version}
find . -name "*.class" -delete
find . -name "*.jar" -type f -print -delete

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Unavailable
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :taglist-maven-plugin
%pom_remove_plugin :emma-maven-plugin

# Unwanted
%pom_remove_plugin :maven-source-plugin

# Remove org.jvnet.wagon-svn:wagon-svn
%pom_xpath_remove "pom:build/pom:extensions"

%pom_xpath_remove "pom:dependencies/pom:dependency[pom:scope='test']"

# Fix http://jira.codehaus.org/browse/MCOMPILER-130
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/pom:compilerArgument"
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration" "
<compilerArgument>-Werror</compilerArgument>"
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration" "
<compilerArgument>-Xlint:all</compilerArgument>"

# remove bundled Doug Lea JCP JSR-166
rm -r src/main/java/com/googlecode/concurrentlinkedhashmap/ConcurrentHashMapV8.java
sed -i "s|ConcurrentHashMapV8|java.util.concurrent.ConcurrentHashMap|" \
 src/main/java/com/googlecode/concurrentlinkedhashmap/ConcurrentLinkedHashMap.java

# Fix mojo-signatures aId
#sed -i "s|jdk.version}-sun</artifactId>|jdk.version}</artifactId>|" pom.xml
# Disabled currently is broken
%pom_remove_plugin :animal-sniffer-maven-plugin

%mvn_file :%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# test skipped for unavailable test deps
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Mon Oct 17 2016 Tomas Repik <trepik@redhat.com> - 1.4.2-5
- use standard SCL macros

* Wed Jul 27 2016 Tomas Repik <trepik@redhat.com> - 1.4.2-4
- scl conversion

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 gil cattaneo <puntogil@libero.it> 1.4.2-1
- update to 1.4.2

* Fri Jan 30 2015 gil cattaneo <puntogil@libero.it> 1.3.2-6
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.3.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 gil cattaneo <puntogil@libero.it> 1.3.2-2
- switch to XMvn
- minor changes to adapt to current guideline

* Thu May 23 2013 gil cattaneo <puntogil@libero.it> 1.3.2-1
- update to 1.3.2

* Wed Sep 26 2012 gil cattaneo <puntogil@libero.it> 1.3.1-1
- initial rpm
