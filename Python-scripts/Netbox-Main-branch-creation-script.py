from extras.scripts import *
from django.utils.text import slugify

from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Site


class NewBranchScript(Script):

    class Meta:
        name = "New Branch"
        description = "Provision a new branch site"

    site_name = StringVar(
        description="Name of the new site"
    )
    downstream_switch_count = IntegerVar(
        description="Number of downstream switches to create"
    )
    downstream_switch_model = ObjectVar(
        description="Downstream switch model",
        model=DeviceType
    )
    upstream_switch_count = IntegerVar(
        description="Number of upstream switches to create"
    )
    upstream_switch_model = ObjectVar(
        description="Upstream switch model",
        model=DeviceType
    )
    router_count = IntegerVar(
        description="Number of routers to create"
    )
    router_model = ObjectVar(
        description="Router model",
        model=DeviceType
    )
    server_count = IntegerVar(
        description="Number of QOE servers to create"
    )
    server_model = ObjectVar(
        description="Server model",
        model=DeviceType
    )
    corero_count = IntegerVar(
        description="Number of Corero to create"
    )
    corero_model = ObjectVar(
        description="Corero model",
        model=DeviceType
    )
    management_count = IntegerVar(
        description="Number of Management switch to create"
    )
    management_model = ObjectVar(
        description="Management Switch model",
        model=DeviceType
    )
    cable_mgmt_count = IntegerVar(
        description="Number of Cable Management to create"
    )
    cable_mgmt_model = ObjectVar(
        description="Cable management model",
        model=DeviceType
    )
    opengear_count = IntegerVar(
        description="Number of OpenGear to create"
    )
    opengear_model = ObjectVar(
        description="OpenGear model",
        model=DeviceType
    )
    def run(self, data, commit):

        # Create the new site
        site = Site(
            name=data['site_name'],
            slug=slugify(data['site_name']),
            status=SiteStatusChoices.STATUS_ACTIVE,
        )
        site.save()
        self.log_success(f"Created new site: {site}")

        # Create downstream switches
        downstream_switch_role = DeviceRole.objects.get(name='L3 Switch')
        for i in range(1, data['downstream_switch_count'] + 1):
            downstream_switch = Device(
                device_type=data['downstream_switch_model'],
                name=f'{site.slug.upper()}-DNSTRM-SW{i}',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=downstream_switch_role
            )
            downstream_switch.save()
            self.log_success(f"Created new downstream switch: {downstream_switch}")

        # Create upstream switches
        upstream_switch_role = DeviceRole.objects.get(name='L3 Switch')
        for i in range(1, data['upstream_switch_count'] + 1):
            upstream_switch = Device(
                device_type=data['upstream_switch_model'],
                name=f'{site.slug.upper()}-UPSTRM-SW{i}',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=upstream_switch_role
            )
            upstream_switch.save()
            self.log_success(f"Created new switch: {upstream_switch}")

        # Create routers
        router_role = DeviceRole.objects.get(name='Core Router')
        for i in range(1, data['router_count'] + 1):
            router = Device(
                device_type=data['router_model'],
                name=f'{site.slug.upper()}-CR-RTR-{i}',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=router_role
            )
            router.save()
            self.log_success(f"Created new router: {router}")

        # Create Servers
        server_role = DeviceRole.objects.get(name='QOE')
        for i in range(1, data['server_count'] + 1):
            server = Device(
                device_type=data['server_model'],
                name=f'{site.slug.upper()}-QOE-{i}',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=server_role
            )
            server.save()
            self.log_success(f"Created new server: {server}")

        # Create Corero
        corero_role = DeviceRole.objects.get(name='Firewall')
        for i in range(1, data['corero_count'] + 1):
            corero = Device(
                device_type=data['corero_model'],
                name=f'{site.slug.upper()}-Corero',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=corero_role
            )
            corero.save()
            self.log_success(f"Created new server: {corero}")

        # Create Management Switch
        management_role = DeviceRole.objects.get(name='Management Switch')
        for i in range(1, data['management_count'] + 1):
            management_switch = Device(
                device_type=data['management_model'],
                name=f'{site.slug.upper()}-MTIK-MGMT-SW',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=management_role
            )
            management_switch.save()
            self.log_success(f"Created new server: {management_switch}")

        # Create Cable Management
        cable_mgmt_role = DeviceRole.objects.get(name='Cable Management')
        for i in range(1, data['cable_mgmt_count'] + 1):
            cable_mgmt = Device(
                device_type=data['cable_mgmt_model'],
                name=f'{site.slug.upper()}-Rack1-Cable Management',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=cable_mgmt_role
            )
            cable_mgmt.save()
            self.log_success(f"Created new server: {cable_mgmt}")

        # Create OpenGear Console
        opengear_role = DeviceRole.objects.get(name='Console')
        for i in range(1, data['opengear_count'] + 1):
            opengear = Device(
                device_type=data['opengear_model'],
                name=f'{site.slug.upper()}-OpenGear-Console',
                site=site,
                status=DeviceStatusChoices.STATUS_ACTIVE,
                device_role=opengear_role
            )
            opengear.save()
            self.log_success(f"Created new server: {opengear}")

        # Generate a CSV table of new devices
        output = [
            'name,make,model'
        ]
        for device in Device.objects.filter(site=site):
            attrs = [
                device.name,
                device.device_type.manufacturer.name,
                device.device_type.model
            ]
            output.append(','.join(attrs))

        return '\n'.join(output)
