from dataclasses import dataclass

from django.db.models import Count
from .models import Group, Service, Team, Template

@dataclass
class ReportEntry:
    team: Team
    group_count: int
    service_count: int
    template_count: int

def team_report():
    """
        Generate team report
    """
    data = []
    
    querySet = Team.objects.values("nome").annotate(
        group_count=Count(Group),        # substituir "Group" por query que busca os grupos da equipe
        service_count=Count(Service),    # substituir "Service" por query que busca os serviços do grupo
        template_count=Count(Template),   # substituir "Template" por query que busca os templates do grupo
    )
    
    equipes_index = {}
    for equipe in Team.objects.all():
        equipes_index[equipe.pk] = equipe
    
    for entry in querySet:
        equipe = equipes_index.get(entry['nome'])
        report_entry = ReportEntry(
            team=equipe,
            group_count=entry['group_count'],
            service_count=entry['service_count'],
            template_count=entry['template_count']
        )

        data.append(report_entry)
        
    return data