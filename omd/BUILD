# List of Packages that are installed into intermediate install.
# This should be extended to all packages once there is a target
# to create dest, since intermediate install can be removed at
# that point.
PACKAGES_EXT = [
    "freetds",
    "rrdtool",
]

PACKAGES_EXT_LABEL = ["@%s//:%s" % (p, p) for p in PACKAGES_EXT]

PACKAGES_INT = [
    "//omd/packages/Python:python_tar_with_prefix",
    "//omd/packages/openssl:openssl_with_prefix_tar",
    "//omd/packages/net-snmp:net-snmp_with_prefix_tar",
    "//omd/packages/perl-modules:perl-modules.tar",
    "//omd/packages/python3-modules:python3-modules.tar",
    "//packages/cmk-agent-based:pkg_tar",
    "//packages/cmk-werks:pkg_tar",
    "//packages/cmk-mkp-tool:pkg_tar",
    "//packages/cmk-crypto:pkg_tar",
    "//packages/cmk-agent-receiver:pkg_tar",
    "//packages/cmk-graphing:pkg_tar",
    "//packages/cmk-messaging:pkg_tar",
    "//packages/cmk-rulesets:pkg_tar",
    "//packages/cmk-server-side-calls:pkg_tar",
    "//packages/cmk-livestatus-client:cmk_livestatus_client_pkg_tar",
    "//packages/cmk-livestatus-client:cmk_livestatus_pkg_tar",
    "//packages/cmk-trace:pkg_tar",
]

genrule(
    name = "intermediate_install",
    srcs = PACKAGES_EXT_LABEL + PACKAGES_INT,
    outs = ["intermediate_install.tar.gz"],
    cmd = """
        set -x
        echo $$PWD
        ls -lah
        mkdir intermediate_install
        for F in $(SRCS); do
            if [[ "$$F" == *.tar ]];
            then
                tar -xf $$F -C intermediate_install
            elif [[ $$(ls $$F/*.tar) == *.tar ]]
            then
                tar -xf $$F/*.tar -C intermediate_install
            fi
        done

        # package created files into archive
        tar cf $@ intermediate_install
    """,
)
