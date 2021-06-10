from winrm.protocol import Protocol

p = Protocol(
    endpoint='https://192.168.1.100:5986/wsman',
    transport='ntlm',
    username=r'somedomain\someuser',
    password='secret',
    server_cert_validation='ignore')
shell_id = p.open_shell()
command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
p.cleanup_command(shell_id, command_id)
p.close_shell(shell_id)
print(stdout_out)
