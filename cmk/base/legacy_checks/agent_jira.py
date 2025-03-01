#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# {'jql': [{'service_description': 'My summed up field', 'result': ('sum',
# ('customfield_1000', 1000)), 'query': 'project = my_project and status =
# closed'}, {'service_description': 'My counted field', 'result': 'count',
# 'query': 'project = my_project and status = "waiting for something"'},
# {'service_description': 'My averaged field', 'result': ('average',
# ('customfield_1001', 1000)), 'query': 'project = my_project and status =
# open'}], 'password': ('password', 'my_password'), 'protocol': 'https',
# 'user': 'my_user', 'project_workflows': [('my_project', ['in progress'])]}


from collections.abc import Mapping, Sequence
from typing import Any

from cmk.base.config import special_agent_info

from cmk.agent_based.v0_unstable_legacy import passwordstore_get_cmdline


def _get_project_workflow(project_values, prefix):
    options = []
    for key, values in project_values:
        options.append("--%s-key" % prefix)
        options.append(key)
        options.append("--%s-values" % prefix)
        options += values
    return options


def _get_custom_query(jql_values, prefix):
    options = []
    for values in jql_values:
        options.append("--%s-desc" % prefix)
        options.append(values["service_description"])
        options.append("--%s-query" % prefix)
        options.append(values["query"])
        options.append("--%s-result" % prefix)
        if isinstance(values["result"], tuple):
            options.append(values["result"][0])
            options.append("--%s-field" % prefix)
            options.append(values["result"][1][0])
            options.append("--%s-limit" % prefix)
            options.append("%d" % values["result"][1][1])
        else:
            options.append(values["result"])
            options.append("--%s-field" % prefix)
            options.append("None")
            options.append("--%s-limit" % prefix)
            options.append("0")
    return options


def agent_jira_arguments(
    params: Mapping[str, Any], hostname: str, ipaddress: str | None
) -> Sequence[str | tuple[str, str, str]]:
    args = [
        "-P",
        params["protocol"],
        "-u",
        params["user"],
        "-s",
        passwordstore_get_cmdline("%s", params["password"]),
    ]

    args += _get_custom_query(params.get("jql", []), "jql")
    args += _get_project_workflow(params.get("project_workflows", []), "project-workflows")

    if "instance" in params:
        hostname = params["instance"]

    args += [
        "--hostname",
        hostname,
    ]

    return args


special_agent_info["jira"] = agent_jira_arguments
