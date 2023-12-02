#!/bin/bash

PLANNER="/home/software/planners/pandaPI/pandasolver"

DOMAIN_FILE="./dominios/wfc.hddl"
DOMAIN=`cat $DOMAIN_FILE`

PROBLEM_DEST="/tmp/problema.pddl"
DOMAIN_DEST="/tmp/domain.pddl"
# LOCAL_SAS_PLAN="/tmp/output_a190030879.sas"

ARGS="$@"
PLANNER_WITH_ARGS="${PLANNER_ARGS} ${ARGS}"

cat wfc.py | sed -e "s@<alterar_planejador>@$PLANNER_WITH_ARGS@g" \
                 -e "s@<alterar_local_problema>@$PROBLEM_DEST@g" \
                 -e "s@<alterar_local_dominio>@$DOMAIN_DEST@g" \
                 # -e "s@<alterar_local_sas_plan>@$LOCAL_SAS_PLAN@g" \
                 -e "s@<alterar_dominio>@`echo $DOMAIN`@g" > wfc.py3
