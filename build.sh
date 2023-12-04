#!/bin/bash

PLANNER="/home/software/planners/pandaPI/pandasolver"
# PLANNER="/home/esw/a190030879/PandaDealer/problemSolver.sh"

DOMAIN_FILE="./dominios/wfc.hddl"
DOMAIN=`cat $DOMAIN_FILE`

PROBLEM_DEST="./tmp/problema.hddl"
DOMAIN_DEST="./tmp/domain.hddl"
SOLUTION_DEST="./tmp/problem.solution"

ARGS="$@"
PLANNER_WITH_ARGS="${PLANNER} ${ARGS}"

cat wfc.py | sed -e "s@<alterar_planejador>@$PLANNER_WITH_ARGS@g" \
                 -e "s@<alterar_local_problema>@$PROBLEM_DEST@g" \
                 -e "s@<alterar_local_dominio>@$DOMAIN_DEST@g" \
                 -e "s@<alterar_local_solucao>@$SOLUTION_DEST@g" \
                 -e "s@<alterar_dominio>@`echo $DOMAIN`@g" > wfc.py3
