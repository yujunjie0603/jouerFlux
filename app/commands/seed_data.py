import random
import click
from faker import Faker

from app.extensions import db
from app.models import Firewall, Policy, Rule
from app.utils.schema import ActionEnum, ProtocolEnum

fake = Faker()

PORT_POOL = [22, 53, 80, 123, 443, 1024, 1433, 1521, 2049, 2379, 2380, 3306, 5432, 5601, 6379, 8080, 9200]
CIDR_CHOICES = ["0.0.0.0/0", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]

def _random_ip():
    # 源地址偶尔给 CIDR / IPv6，增加随机性
    from random import random as r
    if r() < 0.25:
        return random.choice(CIDR_CHOICES)
    if r() < 0.15:
        return fake.ipv6()
    return fake.ipv4()

def _random_private_dst():
    return fake.ipv4_private()

@click.command("seed")
@click.option("--firewalls", default=100, show_default=True, type=int, help="要创建的防火墙数量")
@click.option("--policies", default=3, show_default=True, type=int, help="每个防火墙的策略数量")
@click.option("--rules", default=5, show_default=True, type=int, help="每个策略的规则数量")
@click.option("--reset", is_flag=True, help="执行前 drop_all + create_all（危险）")
def seed_command(firewalls: int, policies: int, rules: int, reset: bool):
    """
    批量生成初始数据：
    例如：100 防火墙 × 3 策略 × 5 规则 ≈ 1500 条规则
    用法：flask seed --firewalls 100 --policies 3 --rules 5 --reset
    """
    if reset:
        click.echo(" Dropping & creating all tables ...")
        db.drop_all()
        db.create_all()

    total_policies = 0
    total_rules = 0

    # 注意：Policy.name 全局唯一，因此名中带上防火墙索引避免冲突
    for i in range(1, firewalls + 1):
        fw = Firewall(name=f"fw-{i:03d}")
        db.session.add(fw)

        for j in range(1, policies + 1):
            policy = Policy(name=f"policy-fw{i:03d}-{j:02d}")
            fw.policies.append(policy)
            db.session.add(policy)
            total_policies += 1

            for _ in range(rules):
                protocol = random.choice(list(ProtocolEnum))
                action = random.choice(list(ActionEnum))

                # 如果有 ICMP，就不给端口；否则一律给常见端口
                port = None
                if hasattr(ProtocolEnum, "ICMP"):
                    if protocol.name != "ICMP":
                        port = random.choice(PORT_POOL)
                else:
                    port = random.choice(PORT_POOL)

                rule = Rule(
                    action=action,
                    protocol=protocol,
                    source_ip=_random_ip(),
                    destination_ip=_random_private_dst(),
                    port=port,
                    policy=policy
                )
                db.session.add(rule)
                total_rules += 1

        # 分批 flush，降低内存占用 & 更快看到进度
        if i % 25 == 0:
            db.session.flush()
            click.echo(f"…progress: firewalls={i}, policies≈{i*policies}, rules≈{i*policies*rules}")

    db.session.commit()
    click.echo(f" Done! Firewalls={firewalls}, Policies={total_policies}, Rules={total_rules}")