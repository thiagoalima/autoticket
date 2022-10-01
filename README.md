# autoticket

O sistema *Autoticket* permite que o time de Infraestrutura provisione automaticamente chamados a partir de templates pré-configurados, com códigos em ansible.

## Entidades do sistema:
- *Equipes*: equipes de usuários de infraestrutura. Cada equipe pode possuir vários grupos.
- *Grupos*: times específicos pertencentes as equipes. Cada grupo é responsável por um conjunto específico de serviços.
- *Serviços*: atividades relacionadas aos chamados.
- *Templates*: arquivo padrão de código ansible.

## Ferramentas:
- Python
- Django
- API REST
- PostgreSQL
- Git e Github
