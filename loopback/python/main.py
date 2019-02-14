import ncs

class ServiceCallbacks(ncs.application.Service):

    @ncs.application.Service.create
    def cb_create(self, tctx, root, service, proplist):

        self.log.info('Service create(service=', service._path, ')')
        vars = ncs.template.Variables()
        template = ncs.template.Template(service)

        dev = root.devices.device[service.device]

        vars.add('DEVICE', service.device)
        vars.add('DEVICE_TYPE', dev.device_type.cli.ned_id)

        for intf in service.loopback_intf:
            vars.add('INTERFACE', intf.intf)
            vars.add('ADDRESS', intf.ip_address)
            template.apply('loopback-template', vars)

        return proplist


class Main(ncs.application.Application):
    def setup(self):
        self.register_service('loopback', ServiceCallbacks)
