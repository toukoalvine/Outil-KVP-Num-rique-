import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import uuid

# Configuration de la page
st.set_page_config(
    page_title="Outil KVP Numérique",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour un meilleur design
st.markdown("""
<style>
    .pdca-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .phase-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    
    .plan-card { border-left-color: #FF6B6B; background-color: #FFE5E5; }
    .do-card { border-left-color: #4ECDC4; background-color: #E5F9F6; }
    .check-card { border-left-color: #45B7D1; background-color: #E5F3FF; }
    .act-card { border-left-color: #96CEB4; background-color: #E5F5E5; }
    
    .task-completed { text-decoration: line-through; opacity: 0.6; }
    .priority-high { border-left: 3px solid #FF4444; }
    .priority-medium { border-left: 3px solid #FFA500; }
    .priority-low { border-left: 3px solid #4CAF50; }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation du Session State
def init_session_state():
    if 'projects' not in st.session_state:
        st.session_state.projects = {}
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'Administrateur'  # Simplifié pour la démo
    if 'tasks' not in st.session_state:
        st.session_state.tasks = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

# Créer des données d'exemple
def create_sample_project():
    sample_id = str(uuid.uuid4())
    return {
        'id': sample_id,
        'name': 'Exemple : Réduction des temps d\'attente',
        'description': 'Réduire les temps d\'attente en production de 30%',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'en_cours',
        'plan': {
            'problem': 'Temps d\'attente longs entre les étapes de production',
            'goal': 'Réduire les temps d\'attente de 30%',
            'root_cause': 'Capacités des machines déséquilibrées',
            'measures': ['Analyse des machines', 'Optimisation des processus', 'Formation']
        },
        'do': {
            'implementation_steps': [
                {'task': 'Analyser l\'utilisation des machines', 'responsible': 'Marie Dupont', 'due_date': '2024-07-15', 'status': 'terminé'},
                {'task': 'Identifier les goulots d\'étranglement', 'responsible': 'Pierre Martin', 'due_date': '2024-07-20', 'status': 'en_cours'},
                {'task': 'Implémenter les mesures d\'optimisation', 'responsible': 'Sophie Bernard', 'due_date': '2024-07-30', 'status': 'ouvert'}
            ]
        },
        'check': {
            'metrics': {'temps_attente_avant': 45, 'temps_attente_apres': 32, 'amelioration_pourcentage': 28.9},
            'results': 'Les temps d\'attente ont pu être réduits de 28,9%'
        },
        'act': {
            'standardization': 'Nouvelles instructions de travail créées',
            'lessons_learned': 'L\'analyse régulière des capacités est essentielle',
            'next_steps': 'Extension à d\'autres lignes de production'
        }
    }

# Calcul du progrès
def calculate_progress(project_data):
    phases = ['plan', 'do', 'check', 'act']
    completed_phases = 0
    
    if project_data.get('plan', {}).get('problem'):
        completed_phases += 0.25
    if project_data.get('do', {}).get('implementation_steps'):
        completed_phases += 0.25
    if project_data.get('check', {}).get('results'):
        completed_phases += 0.25
    if project_data.get('act', {}).get('standardization'):
        completed_phases += 0.25
    
    return min(completed_phases * 100, 100)

# Affichage du progrès PDCA
def show_pdca_progress(current_phase):
    phases = ['Planifier', 'Faire', 'Vérifier', 'Agir']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    phase_keys = ['plan', 'do', 'check', 'act']
    
    cols = st.columns(4)
    for i, (phase, color, key) in enumerate(zip(phases, colors, phase_keys)):
        with cols[i]:
            if key == current_phase:
                st.markdown(f"""
                <div style="background-color: {color}; color: white; padding: 10px; 
                           border-radius: 5px; text-align: center; font-weight: bold;">
                    {phase} ✓
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f0f0f0; color: #666; padding: 10px; 
                           border-radius: 5px; text-align: center;">
                    {phase}
                </div>
                """, unsafe_allow_html=True)

# Application principale
def main():
    init_session_state()
    
    # En-tête
    st.markdown('<div class="pdca-header">🔄 Outil KVP Numérique</div>', unsafe_allow_html=True)
    
    # Barre latérale pour la sélection de projet
    with st.sidebar:
        st.header("Sélection de Projet")
        
        # Créer un nouveau projet
        if st.button("➕ Nouveau Projet"):
            new_project = {
                'id': str(uuid.uuid4()),
                'name': 'Nouveau Projet KVP',
                'description': '',
                'created_date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'brouillon',
                'plan': {}, 'do': {}, 'check': {}, 'act': {}
            }
            st.session_state.projects[new_project['id']] = new_project
            st.session_state.current_project = new_project['id']
            st.rerun()
        
        # Ajouter un projet d'exemple
        if st.button("📝 Charger Projet d'Exemple"):
            sample = create_sample_project()
            st.session_state.projects[sample['id']] = sample
            st.session_state.current_project = sample['id']
            st.rerun()
        
        # Liste des projets
        if st.session_state.projects:
            project_names = {pid: proj['name'] for pid, proj in st.session_state.projects.items()}
            selected_project = st.selectbox(
                "Projet Actif :",
                options=list(project_names.keys()),
                format_func=lambda x: project_names[x],
                index=0 if st.session_state.current_project is None else 
                      list(project_names.keys()).index(st.session_state.current_project) 
                      if st.session_state.current_project in project_names else 0
            )
            st.session_state.current_project = selected_project
        
        # Rôle utilisateur
        st.selectbox("Rôle Utilisateur :", ['Administrateur', 'Éditeur', 'Lecteur'], 
                    index=['Administrateur', 'Éditeur', 'Lecteur'].index(st.session_state.user_role),
                    key='user_role')
    
    # Contenu principal
    if not st.session_state.projects:
        st.info("👋 Bienvenue ! Créez un nouveau projet ou chargez le projet d'exemple.")
        
        # Information d'intégration
        with st.expander("🎯 Tour de l'Outil : Comment fonctionne l'Outil KVP"):
            st.markdown("""
            **1. Cycle PDCA :** Travaillez de manière structurée à travers les quatre phases
            - **Planifier :** Définir le problème et planifier les mesures
            - **Faire :** Mettre en œuvre et suivre les mesures
            - **Vérifier :** Examiner et évaluer les résultats
            - **Agir :** Standardiser et définir les prochaines étapes
            
            **2. Suivi des Tâches :** Gérer les tâches avec responsabilités et échéances
            **3. Visualisation :** Tableaux de bord et suivi des progrès
            **4. Travail d'Équipe :** Commentaires et collaboration
            """)
        return
    
    # Afficher le projet actuel
    current_proj = st.session_state.projects[st.session_state.current_project]
    
    # En-tête du projet avec progrès
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.header(current_proj['name'])
        if st.session_state.user_role in ['Administrateur', 'Éditeur']:
            new_name = st.text_input("Nom du Projet :", current_proj['name'], key="proj_name")
            if new_name != current_proj['name']:
                current_proj['name'] = new_name
    
    with col2:
        progress = calculate_progress(current_proj)
        st.metric("Progrès", f"{progress:.0f}%")
    
    with col3:
        status_options = ['brouillon', 'en_cours', 'terminé', 'en_attente']
        status_labels = {'brouillon': '📝 Brouillon', 'en_cours': '🔄 En Cours', 
                        'terminé': '✅ Terminé', 'en_attente': '⏸️ En Attente'}
        if st.session_state.user_role in ['Administrateur', 'Éditeur']:
            new_status = st.selectbox("Statut :", status_options, 
                                    index=status_options.index(current_proj.get('status', 'brouillon')),
                                    format_func=lambda x: status_labels[x])
            current_proj['status'] = new_status
    
    # Onglets pour les phases PDCA
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Planifier", "🔨 Faire", "📊 Vérifier", "🎯 Agir", "📈 Tableau de Bord"])
    
    with tab1:  # PLAN
        st.markdown('<div class="phase-card plan-card"><h3>📋 Planifier - Planification</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('plan')
        
        if st.session_state.user_role in ['Administrateur', 'Éditeur']:
            # Définition du problème
            st.subheader("🎯 Définition du Problème")
            problem = st.text_area("Quel est le problème ?", 
                                 current_proj.get('plan', {}).get('problem', ''),
                                 help="Décrivez le problème de manière concrète et mesurable")
            
            # Définition des objectifs
            st.subheader("🎯 Définition des Objectifs")
            goal = st.text_area("Quel est l'objectif ?", 
                              current_proj.get('plan', {}).get('goal', ''),
                              help="Objectifs SMART : Spécifiques, Mesurables, Atteignables, Pertinents, Temporels")
            
            # Analyse des causes
            st.subheader("🔍 Analyse des Causes")
            root_cause = st.text_area("Quelles sont les causes principales ?", 
                                    current_proj.get('plan', {}).get('root_cause', ''),
                                    help="Utilisez les 5 Pourquoi, le diagramme d'Ishikawa ou d'autres méthodes d'analyse")
            
            # Planification des mesures
            st.subheader("📝 Planification des Mesures")
            measures_text = st.text_area("Mesures prévues (une par ligne) :", 
                                       '\n'.join(current_proj.get('plan', {}).get('measures', [])))
            measures = [m.strip() for m in measures_text.split('\n') if m.strip()]
            
            # Sauvegarde automatique
            if 'plan' not in current_proj:
                current_proj['plan'] = {}
            current_proj['plan'].update({
                'problem': problem,
                'goal': goal,
                'root_cause': root_cause,
                'measures': measures
            })
        else:
            # Affichage seul pour les lecteurs
            plan_data = current_proj.get('plan', {})
            if plan_data.get('problem'):
                st.write("**Problème :**", plan_data['problem'])
            if plan_data.get('goal'):
                st.write("**Objectif :**", plan_data['goal'])
            if plan_data.get('root_cause'):
                st.write("**Causes :**", plan_data['root_cause'])
            if plan_data.get('measures'):
                st.write("**Mesures :**")
                for measure in plan_data['measures']:
                    st.write(f"• {measure}")
    
    with tab2:  # DO
        st.markdown('<div class="phase-card do-card"><h3>🔨 Faire - Mise en Œuvre</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('do')
        
        # Gestion des tâches
        st.subheader("📋 Suivi des Tâches")
        
        if st.session_state.user_role in ['Administrateur', 'Éditeur']:
            # Ajouter une nouvelle tâche
            with st.expander("➕ Ajouter une Nouvelle Tâche"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_task = st.text_input("Tâche :")
                with col2:
                    new_responsible = st.text_input("Responsable :")
                with col3:
                    new_date = st.date_input("Date d'Échéance :")
                
                if st.button("Ajouter la Tâche") and new_task:
                    if 'do' not in current_proj:
                        current_proj['do'] = {'implementation_steps': []}
                    if 'implementation_steps' not in current_proj['do']:
                        current_proj['do']['implementation_steps'] = []
                    
                    current_proj['do']['implementation_steps'].append({
                        'task': new_task,
                        'responsible': new_responsible,
                        'due_date': new_date.strftime('%Y-%m-%d'),
                        'status': 'ouvert',
                        'priority': 'moyen'
                    })
                    st.rerun()
        
        # Afficher la liste des tâches
        tasks = current_proj.get('do', {}).get('implementation_steps', [])
        if tasks:
            for i, task in enumerate(tasks):
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                    
                    with col1:
                        task_class = "task-completed" if task['status'] == 'terminé' else ""
                        st.markdown(f'<div class="{task_class}">{task["task"]}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.write(f"👤 {task['responsible']}")
                    
                    with col3:
                        st.write(f"📅 {task['due_date']}")
                    
                    with col4:
                        if st.session_state.user_role in ['Administrateur', 'Éditeur']:
                            status_map = {'ouvert': 'Ouvert', 'en_cours': 'En Cours', 'terminé': 'Terminé'}
                            status_options = ['ouvert', 'en_cours', 'terminé']
                            current_status_index = status_options.index(task['status']) if task['status'] in status_options else 0
                            new_status = st.selectbox("", status_options, 
                                                    index=current_status_index,
                                                    format_func=lambda x: status_map[x],
                                                    key=f"status_{i}")
                            task['status'] = new_status
                    
                    with col5:
                        if st.session_state.user_role == 'Administrateur':
                            if st.button("🗑️", key=f"delete_{i}"):
                                tasks.pop(i)
                                st.rerun()
                    
                    st.divider()
        else:
            st.info("Aucune tâche définie pour le moment.")
    
    with tab3:  # CHECK
        st.markdown('<div class="phase-card check-card"><h3>📊 Vérifier - Vérification</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('check')
        
        if st.session_state.user_role in ['Administrateur', 'Éditeur']:
            st.subheader("📈 Indicateurs & Résultats")
            
            # Saisir les métriques
            col1, col2, col3 = st.columns(3)
            with col1:
                metric1 = st.number_input("Valeur Avant :", 
                                        value=current_proj.get('check', {}).get('metrics', {}).get('temps_attente_avant', 0.0))
            with col2:
                metric2 = st.number_input("Valeur Après :", 
                                        value=current_proj.get('check', {}).get('metrics', {}).get('temps_attente_apres', 0.0))
            with col3:
                if metric1 > 0:
                    improvement = ((metric1 - metric2) / metric1) * 100
                    st.metric("Amélioration", f"{improvement:.1f}%")
            
            # Évaluation des résultats
            results = st.text_area("Évaluation des Résultats :", 
                                 current_proj.get('check', {}).get('results', ''))
            
            # Sauvegarder
            if 'check' not in current_proj:
                current_proj['check'] = {}
            current_proj['check'].update({
                'metrics': {
                    'temps_attente_avant': metric1,
                    'temps_attente_apres': metric2,
                    'amelioration_pourcentage': improvement if metric1 > 0 else 0
                },
                'results': results
            })
        else:
            # Affichage seul
            check_data = current_proj.get('check', {})
            if check_data.get('metrics'):
                metrics = check_data['metrics']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avant", metrics.get('temps_attente_avant', 0))
                with col2:
                    st.metric("Après", metrics.get('temps_attente_apres', 0))
                with col3:
                    st.metric("Amélioration", f"{metrics.get('amelioration_pourcentage', 0):.1f}%")
            
            if check_data.get('results'):
                st.write("**Résultats :**", check_data['results'])
    
    with tab4:  # ACT
        st.markdown('<div class="phase-card act-card"><h3>🎯 Agir - Action</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('act')
        
        if st.session_state.user_role in ['Administrateur', 'Éditeur']:
            st.subheader("📋 Standardisation & Prochaines Étapes")
            
            # Standardisation
            standardization = st.text_area("Standardisation :", 
                                         current_proj.get('act', {}).get('standardization', ''),
                                         help="Comment les améliorations sont-elles ancrées de manière permanente ?")
            
            # Leçons apprises
            lessons = st.text_area("Leçons Apprises :", 
                                 current_proj.get('act', {}).get('lessons_learned', ''),
                                 help="Qu'avez-vous appris ? Que feriez-vous différemment ?")
            
            # Prochaines étapes
            next_steps = st.text_area("Prochaines Étapes :", 
                                    current_proj.get('act', {}).get('next_steps', ''),
                                    help="Quelles mesures de suivi sont prévues ?")
            
            # Sauvegarder
            if 'act' not in current_proj:
                current_proj['act'] = {}
            current_proj['act'].update({
                'standardization': standardization,
                'lessons_learned': lessons,
                'next_steps': next_steps
            })
        else:
            # Affichage seul
            act_data = current_proj.get('act', {})
            if act_data.get('standardization'):
                st.write("**Standardisation :**", act_data['standardization'])
            if act_data.get('lessons_learned'):
                st.write("**Leçons Apprises :**", act_data['lessons_learned'])
            if act_data.get('next_steps'):
                st.write("**Prochaines Étapes :**", act_data['next_steps'])
    
    with tab5:  # DASHBOARD
        st.header("📈 Tableau de Bord du Projet")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        tasks = current_proj.get('do', {}).get('implementation_steps', [])
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t['status'] == 'terminé'])
        in_progress_tasks = len([t for t in tasks if t['status'] == 'en_cours'])
        overdue_tasks = len([t for t in tasks if t['status'] != 'terminé' and 
                           datetime.strptime(t['due_date'], '%Y-%m-%d') < datetime.now()])
        
        with col1:
            st.metric("Total Tâches", total_tasks)
        with col2:
            st.metric("Terminées", completed_tasks, f"{completed_tasks}/{total_tasks}")
        with col3:
            st.metric("En Cours", in_progress_tasks)
        with col4:
            st.metric("En Retard", overdue_tasks, delta=f"-{overdue_tasks}" if overdue_tasks > 0 else None)
        
        # Diagramme de statut des tâches
        if tasks:
            status_counts = {}
            status_labels_fr = {'terminé': 'Terminé', 'en_cours': 'En Cours', 'ouvert': 'Ouvert'}
            for task in tasks:
                status = task['status']
                label = status_labels_fr.get(status, status)
                status_counts[label] = status_counts.get(label, 0) + 1
            
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Répartition du Statut des Tâches",
                color_discrete_map={
                    'Terminé': '#4CAF50',
                    'En Cours': '#FFA500',
                    'Ouvert': '#FF4444'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Évolution temporelle (si des métriques sont disponibles)
        check_data = current_proj.get('check', {}).get('metrics', {})
        if check_data:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Avant', 'Après'],
                y=[check_data.get('temps_attente_avant', 0), check_data.get('temps_attente_apres', 0)],
                marker_color=['#FF6B6B', '#4CAF50']
            ))
            fig.update_layout(title="Amélioration par Comparaison", yaxis_title="Valeur")
            st.plotly_chart(fig, use_container_width=True)
    
    # Fonctions d'export
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Actions")
    
    if st.sidebar.button("📥 Exporter le Projet"):
        project_json = json.dumps(current_proj, indent=2, ensure_ascii=False, default=str)
        st.sidebar.download_button(
            label="💾 Télécharger JSON",
            data=project_json,
            file_name=f"projet_kvp_{current_proj['name'].replace(' ', '_')}.json",
            mime="application/json"
        )
    
    if st.sidebar.button("🗑️ Supprimer le Projet") and st.session_state.user_role == 'Administrateur':
        if len(st.session_state.projects) > 1:
            del st.session_state.projects[st.session_state.current_project]
            st.session_state.current_project = list(st.session_state.projects.keys())[0]
            st.rerun()
        else:
            st.sidebar.error("Le dernier projet ne peut pas être supprimé.")

if __name__ == "__main__":
    main()
