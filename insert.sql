INSERT INTO public.iac_inventoryparameter("name", description, value, type_id)
VALUES
('ansible_connection', 'Tipo de conexão utilizada para acessar o host (ssh, local, etc.).','local, ssh, paramiko, winrm, docker, jail, lxc, lxd, smart',4),
('ansible_user', 'Usuário utilizado para acessar o host.',null,1),
('ansible_password', 'Senha utilizada para autenticar o usuário (recomenda-se não usar senhas em texto claro).', null, 3),
('ansible_ssh_private_key_file', 'Caminho para o arquivo de chave privada utilizada para autenticar o usuário.', null, 5),
('ansible_python_interpreter', 'Caminho para o interpretador Python utilizado para executar os módulos do Ansible.', null, 1),
('ansible_port', 'Porta utilizada para acessar o host (padrão é 22 para SSH).', null, 1),
('ansible_ssh_common_args', 'Argumentos adicionais a serem passados para o comando SSH.', null, 1),
('ansible_become', 'Indica se é necessário executar com privilégios elevados (como root).','true,false',4),
('ansible_become_method', 'Método utilizado para elevar os privilégios (sudo, su, pfexec, etc.).','sudo, su, pbrun, pfexec, runas',4),
('ansible_become_user', 'Usuário utilizado para elevar os privilégios. Note que esse usuário deve ter permissão para executar com privilégios elevados no host.', null,1),
('ansible_become_password', 'Senha utilizada para elevar os privilégios. Recomenda-se não usar senhas em texto claro.', null, 3),
('ansible_host', 'Endereço IP ou nome DNS do host. Essa opção substitui o endereço definido em hosts.', null, 1);

