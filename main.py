import csv
import random
import click


class Verb:
    def __init__(self, csv_row):
        self.imperative = csv_row.get("imperative")
        self.je = csv_row.get("je")
        self.tu = csv_row.get("tu")
        self.il = csv_row.get("il")
        self.nous = csv_row.get("nous")
        self.vous = csv_row.get("vous")
        self.ils = csv_row.get("ils")
        self.total = 0
        self.success = 0
        self.english = csv_row.get("english")

    def to_dict(self):
        return {
            "imperative": self.imperative,
            "je": self.je,
            "tu": self.tu,
            "il": self.il,
            "nous": self.nous,
            "vous": self.vous,
            "ils": self.ils,
            "english": self.english,
        }


def write_to_csv(verbs, csv_path):
    with open(csv_path, "w") as f:
        w = csv.DictWriter(f, verbs[0].to_dict().keys())
        w.writeheader()
        for verb in verbs:
            w.writerow(verb.to_dict())


def from_csv(csv_path):
    verbs = []
    with open(csv_path, "r") as read_obj:
        csv_dict_reader = csv.DictReader(read_obj)
        for row in csv_dict_reader:
            verbs.append(Verb(csv_row=row))
    return verbs


@click.command()
@click.option("--csv_path", default="group3verbs.csv")
def cli(csv_path):
    verbs = from_csv(csv_path)
    num = click.prompt(f"How many? (max: {len(verbs)})", default=len(verbs))
    random.shuffle(verbs)
    verbs = verbs[0:num]
    i = 1
    for verb in verbs:
        click.echo(f"{verb.imperative} {verb.english} [{i} / {num}]")
        verb.success += prompt_body("je", verb.je)
        verb.success += prompt_body("tu", verb.tu)
        verb.success += prompt_body("il", verb.il)
        verb.success += prompt_body("nous", verb.nous)
        verb.success += prompt_body("vous", verb.vous)
        verb.success += prompt_body("ils", verb.ils)
        verb.total += 6
        i += 1
    total = 0.0
    success = 0.0
    for verb in verbs:
        click.echo(f"{verb.imperative} {verb.success} / {verb.total}")
        total += verb.total
        success += verb.success
    print(f"Total {(success * 100) / total} {success} / {total}")


def prompt_body(body_name, answer):
    je_value = click.prompt(body_name)
    if je_value != answer:
        click.echo(f"X {answer}")
        click.prompt(body_name)
        return 0
    else:
        click.echo(f"V")
        return 1


if __name__ == '__main__':
    cli()
