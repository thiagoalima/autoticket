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

INSERT INTO public.iac_playbookparameter (name, description, value, type_id) VALUES
('gather_facts', 'Define se o Ansible deve coletar fatos sobre o host antes de executar as tarefas.','true,false',4),
('vars', 'Variáveis definidas no nível de playbook e que têm um escopo global.',null,1),
('vars_files', 'Arquivos YAML que contêm variáveis e podem ser referenciados pelo playbook.', null, 5),
('include', 'Inclui outro arquivo YAML ou um arquivo de tarefas.', null, 5),
('when', 'Executa uma tarefa somente quando uma determinada condição é atendida.',null,1),
('ignore_errors', 'Ignora erros de uma tarefa e continua a execução do playbook.', 'true,false',4),
('no_log', 'Impede que a saída de uma tarefa seja registrada.','true,false',4),
('become', 'Se o Ansible deve se tornar outro usuário antes de executar as tarefas.','true,false',4),
('become_user', 'O usuário a se tornar antes de executar as tarefas.', null,1),
('become_method', 'O método de "tornar-se" a ser usado (por exemplo, sudo).', 'sudo, su, pbrun, pfexec, runas',4),
('environment', 'Variáveis definidas no ambiente do sistema operacional, que podem ser acessadas em um playbook com a variável `ansible_env`.', null,1),
('extra_vars', 'Variáveis passadas na linha de comando ao executar o playbook com a opção `-e`.', null,1),
('ignore_unreachable', 'Ignora hosts inacessíveis e continua a execução do playbook.','true,false',4),
('any_errors_fatal', 'Define se o playbook deve parar imediatamente quando qualquer erro ocorre.', null,1),
('connection', 'O tipo de conexão a ser usado para se conectar ao host.', 'local, ssh, paramiko, winrm, docker, jail, lxc, lxd, smart',4),
('remote_user', 'O usuário remoto a ser usado para se conectar ao host.', null,1),
('timeout', 'O tempo limite para a conexão remota.', null,1),
('delegate_facts', 'Define se os fatos coletados durante a execução de uma tarefa devem ser devolvidos para o host de origem ou intermediário.', 'true,false',4),
('run_once', 'Executa a tarefa apenas em um host.','true,false',4),
('serial', 'Especifica o número de hosts a serem executados em paralelo.', null,1);

