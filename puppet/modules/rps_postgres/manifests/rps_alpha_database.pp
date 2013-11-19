class rps_postgres::rps_alpha_database {
    postgresql::server::database { 'rps_alpha':
    }

    postgresql::server::database_grant {'give ubuntu rps_alpha':
        privilege => 'ALL',
        db        => 'rps_alpha',
        role      => 'ubuntu',
        require   => [
            Postgresql::Server::Role['ubuntu'],
            Postgresql::Server::Database['rps_alpha']
        ]
    }

    # FIXME: Everything below here should be controlled with hiera
    postgresql::server::role { 'vagrant': }

    postgresql::server::database_grant {'give vagrant rps_alpha':
        privilege => 'ALL',
        db        => 'rps_alpha',
        role      => 'vagrant',
        require   => [
            Postgresql::Server::Role['vagrant'],
            Postgresql::Server::Database['rps_alpha']
        ]
    }

    postgresql::server::role { 'jenkins': }

    postgresql::server::database_grant {'give jenkins rps_alpha':
        privilege => 'ALL',
        db        => 'rps_alpha',
        role      => 'jenkins',
        require   => [
            Postgresql::Server::Role['jenkins'],
            Postgresql::Server::Database['rps_alpha']
        ]
    }
}
