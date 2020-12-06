# shellcheck disable=SC2164
cd VM1
# shellcheck disable=SC2028
echo "Démarrage VM1\n"
vagrant up

# shellcheck disable=SC2164
cd ../VM3
# shellcheck disable=SC2028
echo "Démarrage VM3\n"
vagrant up

# shellcheck disable=SC2164
cd ../VM2
# shellcheck disable=SC2028
echo "Démarrage VM2\n"
vagrant up

# shellcheck disable=SC2164
cd ../VM1-6
# shellcheck disable=SC2028
echo "Démarrage VM1-6\n"
vagrant up

# shellcheck disable=SC2164
cd ../VM2-6
# shellcheck disable=SC2028
echo "Démarrage VM2-6\n"
vagrant up

# shellcheck disable=SC2164
cd ../VM3-6
# shellcheck disable=SC2028
echo "Démarrage VM3-6\n"
vagrant up