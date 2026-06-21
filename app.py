import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Analyse ACP - Réplication JASP")
st.title("📊 Analyse en Composantes Principales (ACP)")
st.markdown("*Réplication Algorithmique de l'Environnement JASP pour la Recherche Scientifique*")

# =========================================================================
# 📚 DICTIONNAIRE DES QUESTIONS COMPLETES (POUR L'ARTICLE)
# =========================================================================
QUESTIONS_MAP = {
    "(Score_Z)1.1": "1.1 Quelles définitions donner aux trois composantes de traitement dans la production écrite (graphomotrice, orthographique, textuelle) ?",
    "(Score_Z)1.2": "1.2 Quel est le rôle de la mémoire de travail et de la mémoire à long terme dans la production écrite ?",
    "(Score_Z)1.3": "1.3 Comment interagissent les trois composantes de la production écrite (graphomotrice, orthographique, textuelle) au regard de la capacité limitée de traitement des élèves ?",
    "(Score_Z)1.4": "1.4 Qu'est-ce que le processus de planification globale du contenu d'un texte et quel est son rôle dans la production écrite ?",
    "(Score_Z)1.5": "1.5 La planification globale est-elle une étape obligatoire dans la rédaction d’un texte ?",
    "(Score_Z)1.6": "1.6 Quel est le rôle du processus de formulation dans la production écrite ?",
    "(Score_Z)1.7": "1.7 Quel rôle joue le processus de formulation dans l'organisation des différents niveaux et unités linguistiques de la production écrite ?",
    "(Score_Z)1.8": "1.8 Quel est le rôle du processus de révision dans la production écrite ?",
    "(Score_Z)1.9": "1.9 La révision est-elle forcément une étape finale dans la rédaction d’un texte ?",
    "(Score_Z)1.10": "1.10 À quel âge environ la graphomotricité est-elle réellement automatisée ?",
    "(Score_Z)1.11": "1.11 En quoi la graphomotricité influence-t-elle la qualité de la production écrite ?",
    "(Score_Z)1.12": "1.12 Comment les processus rédactionnels se développent-ils ?",
    "(Score_Z)1.13": "1.13 Quel l’ordre d’apparition des processus dans le développement de l'expertise en production écrite chez l’élève ?",
    "(Score_Z)1.14": "1.14 Quel rôle jouent la métacognition et la régulation dans la production écrite ?",
    "(Score_Z)2.1": "2.1 Comment organiser l'enseignement de la production écrite ?",
    "(Score_Z)2.2": "2.2 Pourquoi intégrer une pratique quotidienne d'écriture et de production écrite en classe ?",
    "(Score_Z)2.3": "2.3 Quels sont les apports respectifs des écrits courts et des écrits longs dans l’apprentissage ?",
    "(Score_Z)2.4": "2.4 Comment aider les élèves qui écrivent très peu à produire des textes plus conséquents et de meilleure qualité ?",
    "(Score_Z)2.5": "2.5 Quelle(s) approche(s) pour organiser un exercice rédactionnel court et structurant, permettant aux élèves de comprendre comment planifier le contenu d'un court texte en veillant à l'enchaînement et à la cohérence des idées ?",
    "(Score_Z)2.6": "2.6 Quelle(s) approche(s) pour organiser un exercice rédactionnel court et structurant, permettant aux élèves de produire un texte à partir d’une amorce et d’une conclusion fournies ?",
    "(Score_Z)2.7": "2.7 Quelle(s) approche(s) pour organiser un exercice rédactionnel court et structurant, permettant aux élèves de comprendre comment composer une phrase complexe ?",
    "(Score_Z)2.8": "2.8 Quelle(s) approche(s) pour organiser un exercice rédactionnel court et structurant, qui aide les élèves à formuler un paragraphe cohérent dans un texte ?",
    "(Score_Z)2.9": "2.9 Quel(s) meilleur(s) moyen(s) d'organiser un exercice rédactionnel court et structurant pour apprendre aux élèves à réviser un paragraphe dans un texte ?",
    "(Score_Z)2.10": "2.10 Quelle(s) approche(s) pour organiser un exercice rédactionnel court et structurant, permettant aux élèves de réviser et corriger l'orthographe au fur et à mesure de la production du texte ?",
    "(Score_Z)2.11": "2.11 Quelle(s) approche(s) pour organiser un exercice rédactionnel court et structurant, permettant aux élèves de choisir la phrase la plus précise et la plus expressive parmi un ensemble ?",
    "(Score_Z)2.12": "2.12 Quelle(s) approche(s) pour organiser un exercice rédactionnel court et structurant, permettant aux élèves de sélectionner les mots les plus précis et adaptés aux idées dans une phrase ou un paragraphe ?",
    "(Score_Z)2.13": "2.13 Comment différencier la production écrite en fonction des besoins des élèves ?",
    "(Score_Z)2.14": "2.14 Comment adapter les tâches de production écrite pour répondre aux besoins spécifiques de chaque élève ?",
    "(Score_Z)2.15": "2.15 Quelle est l’importance de l’articulation entre la maîtrise de la langue et les écrits courts structurants ?",
    "(Score_Z)2.16": "2.16 Quel(s) rôle(s) de la copie de mots, de phrases ou de textes dans l’apprentissage de la production écrite au cycle 3 ?",
    "(Score_Z)2.17": "2.17 Quel(s) bénéfice(s) observe-t-on chez les élèves de cycle 3 lorsque la production écrite est travaillée fréquemment en classe ?",
    "(Score_Z)2.18": "2.18 Pourquoi est-il pertinent de travailler l’orthographe lors de la rédaction d’un texte au cycle 3 ?",
    "(Score_Z)2.19": "2.19 Quel(s) impact(s) les émotions peuvent-elles avoir sur la rédaction d’un texte au cycle 3 ?",
    "(Score_Z)3.3": "3.3 Selon vous, quel(s) avantage(s) de la dictée vocale pour la rédaction d’un texte ?",
    "(Score_Z)3.4": "3.4 Selon vous, quel(s) inconvénient(s) possible(s) de la dictée vocale ?",
    "(Score_Z)3.5": "3.5 Selon vous, dans quel(s) cas l’utilisation de la dictée vocale est-elle particulièrement bénéfique ?",
    "(Score_Z)3.6": "3.6 Selon vous, comment optimiser l’usage de la dictée vocale pour la rédaction d’un texte ?",
    "(Score_Z)3.7": "3.7 Selon vous, que peut apporter la dictée vocale dans l’apprentissage de la production écrite ?",
    "(Score_Z)3.8": "3.8 Selon vous, quel(s) avantage(s) du traitement de texte pour la rédaction ?",
    "(Score_Z)3.9": "3.9 Selon vous, quel(s) inconvénient(s) possible(s) de l’utilisation du traitement de texte ?",
    "(Score_Z)3.10": "3.10 Selon vous, pour quels élèves le traitement de texte est-il particulièrement utile ?",
    "(Score_Z)3.11": "3.11 Selon vous, comment optimiser l’utilisation du traitement de texte en classe ?",
    "(Score_Z)3.12": "3.12 Selon vous, quel(s) impact(s) le traitement de texte peut-il avoir sur l’apprentissage de la rédaction ?",
    "(Score_Z)3.13": "3.13 Selon vous, quel(s) avantage(s) d’écrire avec l'outil \"clavier\" plutôt qu’avec l'outil \"stylo\" au cycle 3 ?",
    "(Score_Z)3.14": "3.14 Selon vous, quel(s) inconvénient(s) d’écrire avec l'outil \"clavier\" plutôt qu’avec l'outil \"stylo\" au cycle 3 ?",
    "(Score_Z)3.15": "3.15 Selon vous, à quel moment le clavier peut-il être un outil pertinent pour rédiger ?",
    "(Score_Z)3.16": "3.16 Selon vous, pourquoi la maîtrise du clavier demande-t-elle du temps ?",
    "(Score_Z)3.17": "3.17 Selon vous, quelle(s) stratégie(s) la ou les plus efficace(s) pour apprendre à rédiger avec un clavier au cycle 3 ?",
    "(Score_Z)4.1": "4.1 Quelle approche adopter pour l'évaluation des écrits des élèves ?",
    "(Score_Z)4.2": "4.2 Faut-il corriger toutes les erreurs ou en sélectionner certaines pour la révision ?",
    "(Score_Z)4.3": "4.3 Comment aider les élèves à voir l’utilité de la révision de leurs écrits ?",
    "(Score_Z)4.4": "4.4 Quel terme peut être plus engageant que \"correction\" ?",
    "(Score_Z)4.5": "4.5 Quels critères permettent d’évaluer la qualité d’un texte produit par un élève de cycle 3 ?",
    "(Score_Z)4.6": "4.6 Quelle approche est pertinente pour corriger des erreurs d’orthographe modélisantes à partir des textes produits par les élèves ?"
}
# =========================================================================

# =========================================================================
# ⚙️ MOTEUR MATHÉMATIQUE R/JASP (L'algorithme exact du package 'psych')
# =========================================================================
def jasp_pca(df, n_factors, rotation='promax', pairwise=True, m=4):
    if pairwise:
        R = df.corr().to_numpy()
    else:
        R = df.dropna().corr().to_numpy()

    eigenvalues, eigenvectors = np.linalg.eigh(R)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    unrotated_loadings = eigenvectors[:, :n_factors] * np.sqrt(np.maximum(eigenvalues[:n_factors], 0))
    
    max_idx = np.argmax(np.abs(unrotated_loadings), axis=0)
    signs = np.sign(unrotated_loadings[max_idx, range(n_factors)])
    unrotated_loadings = unrotated_loadings * signs

    uniqueness = 1 - np.sum(unrotated_loadings**2, axis=1)

    if rotation == 'none':
        loadings = unrotated_loadings
    else:
        h = np.sqrt(np.sum(unrotated_loadings**2, axis=1))
        h[h == 0] = 1e-10
        norm_loadings = unrotated_loadings / h[:, np.newaxis]

        p, k = norm_loadings.shape
        RotMap = np.eye(k)
        d = 0
        for _ in range(1000):
            z = np.dot(norm_loadings, RotMap)
            B = z**3 - (1.0/p) * np.dot(z, np.diag(np.sum(z**2, axis=0)))
            u, s, vh = np.linalg.svd(np.dot(norm_loadings.T, B))
            RotMap = np.dot(u, vh)
            dpast = d
            d = np.sum(s)
            if d < dpast * (1 + 1e-5):
                break
                
        varimax_loadings = np.dot(norm_loadings, RotMap) * h[:, np.newaxis]

        if rotation == 'varimax':
            loadings = varimax_loadings
        elif rotation == 'promax':
            Q = varimax_loadings * np.abs(varimax_loadings)**(m-1)
            U = np.linalg.lstsq(varimax_loadings, Q, rcond=None)[0]
            d_inv = np.diag(np.linalg.inv(np.dot(U.T, U)))
            U = np.dot(U, np.diag(np.sqrt(d_inv)))
            loadings = np.dot(varimax_loadings, U)

    max_idx = np.argmax(np.abs(loadings), axis=0)
    signs = np.sign(loadings[max_idx, range(n_factors)])
    loadings = loadings * signs
    
    if rotation != 'none':
        ss_loadings = np.sum(loadings**2, axis=0)
        sort_idx = np.argsort(ss_loadings)[::-1]
        loadings = loadings[:, sort_idx]

    return loadings, eigenvalues, uniqueness

# =========================================================================
# 🖥️ INTERFACE STREAMLIT
# =========================================================================
@st.cache_data
def load_local_data():
    try:
        return pd.read_excel("score Z.xlsx")
    except FileNotFoundError:
        st.error("❌ Le fichier 'score Z.xlsx' est introuvable.")
        return None

df = load_local_data()

if df is not None:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚙️ Paramétrage de l'Analyse Factorielle")
        
        z_columns = [col for col in df.columns if "(Score_Z)" in str(col)]
        
        if not z_columns:
            st.error("Aucune colonne '(Score_Z)' détectée.")
            selected_columns = []
        else:
            selected_columns = st.multiselect("Variables manifestes incluses :", z_columns, default=z_columns)
        
        if len(selected_columns) > 2:
            df_acp = df[selected_columns]
            max_comp = len(selected_columns)
            nb_components = st.slider("Nombre de composantes à extraire :", 1, max_comp, min(15, max_comp))
            rotation_type = st.selectbox("Méthode de rotation :", ["promax", "varimax", "none"], index=0)
            is_pairwise = True
            
            st.markdown("---")
            min_loading = st.slider("Seuil de suppression des saturations absolues < à :", 0.0, 1.0, 0.40)
            order_by_size = st.checkbox("Trier les variables par poids factoriel (Format JASP)", value=True)

    with col2:
        if len(selected_columns) > 2:
            jasp_loadings, ev, uniqueness = jasp_pca(
                df_acp, 
                n_factors=nb_components, 
                rotation=rotation_type, 
                pairwise=is_pairwise
            )
            
            total_var = len(ev)
            unrotated_prop = ev / total_var
            unrotated_cum = np.cumsum(unrotated_prop)
            
            ss_loadings = np.sum(jasp_loadings**2, axis=0)
            rot_prop = ss_loadings / total_var
            rot_cum = np.cumsum(rot_prop)
            
            # --- 1️⃣ CHARACTERISTICS ---
            st.subheader("📋 Caractéristiques des Composantes (Variance Expliquée)")
            columns_multi = pd.MultiIndex.from_tuples([
                ('Solution initiale (non pivotée)', 'Valeur Propre'), ('Solution initiale (non pivotée)', 'Proportion var.'), ('Solution initiale (non pivotée)', 'Cumul'),
                ('Solution pivotée', 'Somme des carrés (Loadings)'), ('Solution pivotée', 'Proportion var.'), ('Solution pivotée', 'Cumul')
            ])
            char_df = pd.DataFrame(index=[f"RC {i+1}" for i in range(nb_components)], columns=columns_multi)
            char_df[('Solution initiale (non pivotée)', 'Valeur Propre')] = ev[:nb_components]
            char_df[('Solution initiale (non pivotée)', 'Proportion var.')] = unrotated_prop[:nb_components]
            char_df[('Solution initiale (non pivotée)', 'Cumul')] = unrotated_cum[:nb_components]
            char_df[('Solution pivotée', 'Somme des carrés (Loadings)')] = ss_loadings
            char_df[('Solution pivotée', 'Proportion var.')] = rot_prop
            char_df[('Solution pivotée', 'Cumul')] = rot_cum
            st.dataframe(char_df.style.format({
                ('Solution initiale (non pivotée)', 'Valeur Propre'): "{:.3f}", ('Solution initiale (non pivotée)', 'Proportion var.'): "{:.5f}", ('Solution initiale (non pivotée)', 'Cumul'): "{:.4f}",
                ('Solution pivotée', 'Somme des carrés (Loadings)'): "{:.3f}", ('Solution pivotée', 'Proportion var.'): "{:.5f}", ('Solution pivotée', 'Cumul'): "{:.4f}"
            }), use_container_width=True)
            
            # --- 2️⃣ SCREE PLOT DYNAMIQUE ---
            st.subheader("📈 Graphique d'Éboulis (Scree Plot) & Critère de Kaiser")
            marker_colors = ['#1f77b4' if val >= 1 else '#bdc3c7' for val in ev] 
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(ev)+1)), y=ev, mode='lines+markers', name='Valeurs Propres',
                line=dict(color='#7f8c8d', width=2), marker=dict(size=12, symbol='circle', color=marker_colors, line=dict(color='white', width=1)),
                customdata=unrotated_prop * 100, hovertemplate="<b>Composante %{x}</b><br>Valeur propre : <b>%{y:.3f}</b><br>Variance expliquée : <b>%{customdata:.2f}%</b><extra></extra>"
            ))
            fig.add_shape(type="line", x0=0.5, y0=1, x1=len(ev)+0.5, y1=1, line=dict(color="#e74c3c", width=2, dash="dash"))
            fig.add_annotation(x=len(ev), y=1.05, text="Critère de Kaiser (VP = 1)", showarrow=False, font=dict(color="#e74c3c", size=13), xanchor="right")
            fig.update_layout(xaxis_title="Composantes (Dimensions Factorielles)", yaxis_title="Valeur Propre (Eigenvalue)", height=600, xaxis=dict(tickmode='linear', dtick=1), margin=dict(l=20, r=20, t=30, b=20), plot_bgcolor='rgba(240, 242, 246, 0.4)')
            st.plotly_chart(fig, use_container_width=True)
            
            # --- 3️⃣ COMPONENT LOADINGS ---
            st.subheader("📋 Matrice des Saturations Factorielles (Component Loadings)")
            loadings_df = pd.DataFrame(jasp_loadings, columns=[f"RC{i+1}" for i in range(nb_components)], index=selected_columns)
            uniqueness_series = pd.Series(uniqueness, index=selected_columns, name="Unicité (Uniqueness)")
            
            if order_by_size:
                max_component = loadings_df.abs().idxmax(axis=1)
                max_value = loadings_df.abs().max(axis=1)
                sort_df = pd.DataFrame({'variable': loadings_df.index, 'max_comp_idx': max_component.map(lambda x: int(x.replace('RC', ''))), 'max_val': max_value}).sort_values(by=['max_comp_idx', 'max_val'], ascending=[True, False])
                loadings_df = loadings_df.reindex(sort_df['variable'])
                uniqueness_series = uniqueness_series.reindex(sort_df['variable'])
            
            filtered_loadings_df = loadings_df.map(lambda x: x if abs(x) >= min_loading else np.nan)
            final_df = pd.concat([filtered_loadings_df, uniqueness_series], axis=1)
            
            st.dataframe(final_df.style.background_gradient(subset=[f"RC{i+1}" for i in range(nb_components)], cmap="coolwarm", vmin=-1, vmax=1).highlight_null(color='white').format("{:.3f}", na_rep=""), height=500, use_container_width=True)

    # =========================================================================
    # 🔬 SECTION DE TRI (POUR L'ARTICLE SCIENTIFIQUE)
    # =========================================================================
    if len(selected_columns) > 2:
        st.markdown("---")
        st.header(" Espace d'Analyse Exploratoire")
        st.markdown("*Outils d'assistance à l'interprétation sémantique des composantes et préparation à la rédaction scientifique.*")

        rc_cols = [f"RC{i+1}" for i in range(nb_components)]
        is_chosen = filtered_loadings_df[rc_cols].notna().any(axis=1)
        chosen_list = final_df[is_chosen]
        excluded_list = final_df[~is_chosen] 

        total_questions = len(selected_columns)
        nb_kept_global = 0
        nb_elim_global = 0
        nb_orphans_global = len(excluded_list)

        # --- 4️⃣ EXPLORATEUR CIBLÉ PAR COMPOSANTE ---
        st.markdown("### 🔍 Examen Isolé des Dimensions Factorielles (RC)")
        st.write("Sélectionnez une composante pour isoler ses variables manifestes afin d'en faciliter l'interprétation thématique :")
        
        selected_rc_target = st.selectbox("Sélection de la composante (RC) :", rc_cols)
        
        if len(chosen_list) > 0:
            target_rc_idx = loadings_df.abs().idxmax(axis=1)
            rc_pure_vars = chosen_list[(target_rc_idx == selected_rc_target)]
            
            if len(rc_pure_vars) > 0:
                st.markdown(f"**Éléments constitutifs majeurs de la {selected_rc_target} :**")
                
                display_target = pd.DataFrame({
                    "Code": rc_pure_vars.index,
                    "Énoncé de la variable (Question)": [QUESTIONS_MAP.get(sub, sub) for sub in rc_pure_vars.index],
                    "Saturation Factorielle": loadings_df.loc[rc_pure_vars.index, selected_rc_target],
                    "Unicité": rc_pure_vars["Unicité (Uniqueness)"]
                }).sort_values(by="Saturation Factorielle", ascending=False)
                
                display_target.set_index("Code", inplace=True)
                
                st.dataframe(
                    display_target.style.format({"Saturation Factorielle": "{:.3f}", "Unicité": "{:.3f}"}), 
                    use_container_width=True,
                    column_config={"Énoncé de la variable (Question)": st.column_config.TextColumn("Énoncé de la variable (Question)", width=900)}
                )
            else:
                st.write(f"Aucune variable ne présente de saturation primaire supérieure au seuil ({min_loading}) sur cette composante.")

        # =========================================================================
        # 📦 5️⃣ CLASSIFICATION ET ARBITRAGE DES COMPOSANTES
        # =========================================================================
        st.markdown("---")
        st.header("🟢🔴Arbitrage Décisionnel et Classification Thématique des Composantes")
        st.write("Répartition finale des dimensions factorielles retenues pour l'élaboration du modèle théorique.")

        target_rc_idx_global = loadings_df.abs().idxmax(axis=1)

        # 🟢 SECTION : BONNES COMPOSANTES
        st.markdown("### 🟢 Dimensions Factorielles Retenues (Inclusion)")
        selected_bons = st.multiselect(
            "Sélectionner les composantes à inclure dans l'analyse finale :", 
            options=rc_cols, 
            default=["RC1", "RC2"] if nb_components >= 2 else rc_cols
        )
        if selected_bons:
            df_bons_rc = final_df[target_rc_idx_global.isin(selected_bons)].copy()
            subset_rcs_bon = [c for c in selected_bons if c in df_bons_rc.columns]
            df_bons_rc = df_bons_rc.dropna(subset=subset_rcs_bon, how='all')
            
            if not df_bons_rc.empty:
                nb_kept_global = len(df_bons_rc)
                df_bons_rc["Code"] = df_bons_rc.index
                df_bons_rc["Énoncé de la variable (Question)"] = [QUESTIONS_MAP.get(idx, idx) for idx in df_bons_rc.index]
                df_bons_rc.set_index("Code", inplace=True)
                
                cols_to_show_bon = ["Énoncé de la variable (Question)"] + subset_rcs_bon + ["Unicité (Uniqueness)"]
                numeric_cols_bon = subset_rcs_bon + ["Unicité (Uniqueness)"]
                config_bon = {"Énoncé de la variable (Question)": st.column_config.TextColumn("Énoncé de la variable (Question)", width=1900)}
                
                st.dataframe(
                    df_bons_rc[cols_to_show_bon].style.background_gradient(
                        subset=subset_rcs_bon, 
                        cmap="coolwarm", vmin=-1, vmax=1
                    ).highlight_null(color='white').format(formatter="{:.3f}", subset=numeric_cols_bon, na_rep=""), 
                    use_container_width=True,
                    column_config=config_bon
                )
                st.success(f"**Synthèse de l'inclusion :** {len(selected_bons)} dimension(s) retenue(s) représentant un corpus de **{nb_kept_global} variables manifestes**.")
            else:
                st.info("Aucune saturation significative n'a été détectée pour ces dimensions.")
        else:
            st.info("Veuillez sélectionner au moins une composante à conserver.")

        st.markdown("<br>", unsafe_allow_html=True)

        # 🔴 SECTION : COMPOSANTES ELIMINEES
        st.markdown("### 🔴 Dimensions Factorielles Écartées (Exclusion)")
        selected_elims = st.multiselect(
            "Sélectionner les composantes à exclure de l'analyse finale :", 
            options=rc_cols
        )
        if selected_elims:
            df_elims_rc = final_df[target_rc_idx_global.isin(selected_elims)].copy()
            subset_rcs_elim = [c for c in selected_elims if c in df_elims_rc.columns]
            df_elims_rc = df_elims_rc.dropna(subset=subset_rcs_elim, how='all')
            
            if not df_elims_rc.empty:
                nb_elim_global = len(df_elims_rc)
                df_elims_rc["Code"] = df_elims_rc.index
                df_elims_rc["Énoncé de la variable (Question)"] = [QUESTIONS_MAP.get(idx, idx) for idx in df_elims_rc.index]
                df_elims_rc.set_index("Code", inplace=True)
                
                cols_to_show_elim = ["Énoncé de la variable (Question)"] + subset_rcs_elim + ["Unicité (Uniqueness)"]
                numeric_cols_elim = subset_rcs_elim + ["Unicité (Uniqueness)"]
                config_elim = {"Énoncé de la variable (Question)": st.column_config.TextColumn("Énoncé de la variable (Question)", width=1900)}
                
                st.dataframe(
                    df_elims_rc[cols_to_show_elim].style.background_gradient(
                        subset=subset_rcs_elim, 
                        cmap="coolwarm", vmin=-1, vmax=1
                    ).highlight_null(color='white').format(formatter="{:.3f}", subset=numeric_cols_elim, na_rep=""), 
                    use_container_width=True,
                    column_config=config_elim
                )
                st.error(f"**Synthèse de l'exclusion :** {len(selected_elims)} dimension(s) écartée(s) représentant un corpus de **{nb_elim_global} variables manifestes**.")
            else:
                st.info("Aucune saturation significative n'a été détectée pour ces dimensions.")
        else:
            st.info("Aucune composante n'est actuellement ciblée pour l'exclusion.")

        # =========================================================================
        # 📊 6️⃣ BILAN GLOBAL FINAL
        # =========================================================================
        st.markdown("---")
        st.header("📊 Synthèse Qualimétrique et Vérification de l'Intégrité du Modèle")
        st.write("Validation du traitement exhaustif du corpus de variables soumises à l'Analyse en Composantes Principales.")
        
        nb_unclassified = total_questions - (nb_kept_global + nb_elim_global + nb_orphans_global)
        
        col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
        col_b1.metric("✅ Variables Retenues", nb_kept_global)
        col_b2.metric("❌ Variables Écartées", nb_elim_global)
        col_b3.metric("👻 Variables Isolées (Absence de saturation forte)", nb_orphans_global, help="Variables dont la variance n'est pas expliquée de manière satisfaisante (saturations < seuil).")
        col_b4.metric("⚠️ Variables Non Classées", nb_unclassified, help="Variables disposant d'une forte saturation mais dont la composante d'appartenance n'a pas encore été arbitrée (Inclusion/Exclusion).")
        col_b5.metric("📌 Taille du Corpus", total_questions)
        
        if nb_unclassified == 0:
            st.success("L'ensemble des variables manifestes a été traité. La classification structurelle du modèle est complète.")
        else:
            st.warning(f"Il reste {nb_unclassified} variable(s) dont le rattachement dimensionnel n'a pas été statué. Veuillez arbitrer toutes les dimensions (RC) générées.")