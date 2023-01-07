cat << EOF >> ~/.ssh/config

Host ${serverLabel}
    HostName ${hostname}
    User ${user}
    IdentityFile ${identityFile}
EOF