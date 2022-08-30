from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path=".", config_name="config")
def my_app(cfg):
    print(cfg)
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()

main
config = Config(os.getcwd() + '/config/')
config_data = config.get_config()

{
  db_solarwinds_sonda: {
    solarwindows_prod: {
      solarwinds_prod: production
      server: 'tcp:192.0.2.183,1435'
      database_solarwinds: SolarWindsOrion
      database_integrator: Integrator
      port: 1435
      username: npmadminsc
      password: dqm50vnc
      driver: ODBC Driver 18 for SQL Server
      trusted_connection: no
      encrypt: no
      trustservercertificate: no
      timeout: 300
      repeat: 3
      sleeptime: 5
    }
  }
  flask_aranda_xxxx:
  itsm_aranda_xxxx:
}

print(config_data['db_solarwinds_sonda']['solarwindows_prod']['server'])
tcp:192.0.2.183,1435
