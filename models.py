# models.py - GHP
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ⭐ Créer db pour les modèles
db = SQLAlchemy()

# ============================================================
# STRUCTURE
# ============================================================
class Structure(db.Model):
    __tablename__ = 'structures'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.Text)
    telephone = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    statut = db.Column(db.String(20), default='en_attente')
    logo_url = db.Column(db.String(500))
    primary_color = db.Column(db.String(7), default='#0d6efd')
    secondary_color = db.Column(db.String(7), default='#6c757d')
    reset_question = db.Column(db.String(255))
    reset_answer_hash = db.Column(db.String(255))
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_activation = db.Column(db.DateTime)
    
    utilisateurs = db.relationship('Utilisateur', backref='structure', lazy=True)
    patients = db.relationship('Patient', backref='structure', lazy=True)


# ============================================================
# UTILISATEUR
# ============================================================
class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    role = db.Column(db.String(50), default='admin')
    structure_id = db.Column(db.Integer, db.ForeignKey('structures.id'))
    actif = db.Column(db.Boolean, default=True)
    reset_token = db.Column(db.String(255))
    reset_token_expiry = db.Column(db.DateTime)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    derniere_connexion = db.Column(db.DateTime)
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


# ============================================================
# PATIENT
# ============================================================
class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, db.ForeignKey('structures.id'), nullable=False)
    
    # Identité
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.Text)
    date_naissance = db.Column(db.Date)
    
    # Assurance principale
    type_assurance = db.Column(db.String(50))
    taux_prise_charge = db.Column(db.Integer, default=0)
    numero_assure = db.Column(db.String(50))
    
    # Assurance complémentaire
    assurance2_nom = db.Column(db.String(100))
    assurance2_type = db.Column(db.String(50), default='complementaire')
    taux_assurance2 = db.Column(db.Numeric, default=0)
    numero_assure2 = db.Column(db.String(100))
    plafond_assurance2 = db.Column(db.Numeric, default=0)
    
    # Personne à prévenir
    personne_a_prevenir_nom = db.Column(db.String(200))
    personne_a_prevenir_telephone = db.Column(db.String(50))
    personne_a_prevenir_relation = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    ventes = db.relationship('Vente', backref='patient', lazy=True)
    factures = db.relationship('Facture', backref='patient', lazy=True)
    rendez_vous = db.relationship('RendezVous', backref='patient', lazy=True)
    proformas = db.relationship('Proforma', backref='patient', lazy=True)


# ============================================================
# ACTES
# ============================================================
class Acte(db.Model):
    __tablename__ = 'actes'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(20))
    nom = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Numeric, nullable=False)
    pbr = db.Column(db.Numeric, default=0)
    description = db.Column(db.Text)
    categorie = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================
# PRODUITS
# ============================================================
class Produit(db.Model):
    __tablename__ = 'produits'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(50))
    nom = db.Column(db.String(200), nullable=False)
    prix_vente = db.Column(db.Numeric, nullable=False)
    prix_achat = db.Column(db.Numeric)
    pbr = db.Column(db.Numeric, default=0)
    quantite_stock = db.Column(db.Integer, default=0)
    seuil_alerte = db.Column(db.Integer, default=10)
    unite = db.Column(db.String(20), default='unité')
    emplacement = db.Column(db.String(50))
    categorie = db.Column(db.String(50))
    fournisseur = db.Column(db.String(100))
    peremption = db.Column(db.Date)
    actif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================
# VENTES
# ============================================================
class Vente(db.Model):
    __tablename__ = 'ventes'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient_nom = db.Column(db.String(200))
    structure_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'pharmacie', 'actes'
    
    # Montants
    sous_total = db.Column(db.Numeric, default=0)
    prise_en_charge = db.Column(db.Numeric, default=0)
    prise_en_charge2 = db.Column(db.Numeric, default=0)
    net_a_payer = db.Column(db.Numeric, default=0)
    base_remboursement = db.Column(db.Numeric, default=0)
    
    # Paiement
    mode_paiement = db.Column(db.String(50))
    montant_donne = db.Column(db.Numeric, default=0)
    rendu = db.Column(db.Numeric, default=0)
    reste_a_payer = db.Column(db.Numeric, default=0)
    
    # Assurances
    taux_assurance = db.Column(db.Integer, default=0)
    assurance = db.Column(db.String(50))
    numero_assure = db.Column(db.String(100))
    assurance2_nom = db.Column(db.String(100))
    taux_assurance2 = db.Column(db.Numeric, default=0)
    numero_assure2 = db.Column(db.String(100))
    taux_temp_modifie = db.Column(db.Boolean, default=False)
    taux_original = db.Column(db.Numeric, default=0)
    
    # Données - ✅ CORRECTION : utiliser JSON au lieu de JSONB
    actes = db.Column(db.JSON)
    produits = db.Column(db.JSON)
    assurances = db.Column(db.JSON, default='[]')
    
    # Métadonnées
    statut = db.Column(db.String(20), default='validee')
    date_vente = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_nom = db.Column(db.String(100))
    vendeur = db.Column(db.String(100))
    
    # Annulation
    annulee_le = db.Column(db.DateTime)
    annulee_par = db.Column(db.Integer)
    motif_annulation = db.Column(db.String(255))
    
    # Relations
    factures = db.relationship('Facture', backref='vente', lazy=True)
    paiements = db.relationship('PaiementFacture', backref='vente', lazy=True)


# ============================================================
# FACTURES
# ============================================================
class Facture(db.Model):
    __tablename__ = 'factures'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient_nom = db.Column(db.String(255), nullable=False)
    patient_telephone = db.Column(db.String(20))
    
    numero_facture = db.Column(db.String(50), nullable=False)
    date_emission = db.Column(db.Date, default=datetime.now().date)
    date_echeance = db.Column(db.Date, nullable=False)
    
    # Montants
    sous_total = db.Column(db.Numeric, default=0)
    taux_assurance = db.Column(db.Numeric, default=0)
    prise_en_charge = db.Column(db.Numeric, default=0)
    taux_assurance2 = db.Column(db.Numeric, default=0)
    prise_en_charge2 = db.Column(db.Numeric, default=0)
    net_a_payer = db.Column(db.Numeric, default=0)
    montant_paye = db.Column(db.Numeric, default=0)
    reste_a_payer = db.Column(db.Numeric, default=0)
    base_remboursement = db.Column(db.Numeric, default=0)
    
    statut = db.Column(db.String(20), default='en_attente')
    articles = db.Column(db.JSON)
    mode_paiement = db.Column(db.String(50))
    notes = db.Column(db.Text)
    assurances_data = db.Column(db.JSON)
    
    vente_id = db.Column(db.Integer, db.ForeignKey('ventes.id'))
    
    created_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    paiements = db.relationship('PaiementFacture', backref='facture', lazy=True)


# ============================================================
# PAIEMENTS FACTURES
# ============================================================
class PaiementFacture(db.Model):
    __tablename__ = 'paiements_factures'
    
    id = db.Column(db.Integer, primary_key=True)
    facture_id = db.Column(db.Integer, db.ForeignKey('factures.id'), nullable=False)
    vente_id = db.Column(db.Integer, db.ForeignKey('ventes.id'))
    montant = db.Column(db.Numeric, nullable=False)
    date_paiement = db.Column(db.DateTime, default=datetime.utcnow)
    mode_paiement = db.Column(db.String(50))
    reference = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(100))
    recu_genere = db.Column(db.Boolean, default=False)


# ============================================================
# FACTURES ASSURANCE
# ============================================================
class FactureAssurance(db.Model):
    __tablename__ = 'factures_assurance'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    mois_reference = db.Column(db.String(7), nullable=False)  # '2024-01'
    assurance = db.Column(db.String(50), nullable=False)
    type_assurance = db.Column(db.String(50), default='principale')
    
    montant_total = db.Column(db.Numeric, nullable=False)
    montant_rembourse = db.Column(db.Numeric, default=0)
    statut = db.Column(db.String(20), default='en_attente')
    
    date_facture = db.Column(db.Date, default=datetime.now().date)
    date_remboursement = db.Column(db.Date)
    details = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================
# PROFORMAS
# ============================================================
class Proforma(db.Model):
    __tablename__ = 'proformas'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient_nom = db.Column(db.String(200), nullable=False)
    patient_telephone = db.Column(db.String(50))
    
    numero_proforma = db.Column(db.Integer)
    type = db.Column(db.String(50), default='mixte')
    
    # Assurances
    assurance_nom = db.Column(db.String(100))
    taux_assurance = db.Column(db.Numeric, default=0)
    numero_assure = db.Column(db.String(100))
    assurance2_nom = db.Column(db.String(100), default='')
    taux_assurance2 = db.Column(db.Numeric, default=0)
    numero_assure2 = db.Column(db.String(50), default='')
    assurance2_active = db.Column(db.Boolean, default=False)
    taux_modifie = db.Column(db.Boolean, default=False)
    taux_original = db.Column(db.Numeric, default=0)
    
    # Montants
    articles = db.Column(db.JSON, default='[]')
    sous_total = db.Column(db.Numeric, default=0)
    prise_en_charge = db.Column(db.Numeric, default=0)
    prise_en_charge2 = db.Column(db.Numeric, default=0)
    net_a_payer = db.Column(db.Numeric, default=0)
    assurances_data = db.Column(db.JSON)
    
    statut = db.Column(db.String(20), default='en_attente')
    vente_id = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    created_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    vue_par_patient = db.Column(db.Boolean, default=False)
    date_vue = db.Column(db.DateTime)


# ============================================================
# PROFORMAS LUNETTES
# ============================================================
class ProformaLunette(db.Model):
    __tablename__ = 'proformas_lunettes'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    patient_nom = db.Column(db.String(200))
    patient_telephone = db.Column(db.String(50))
    patient_date_naissance = db.Column(db.Date)
    patient_age = db.Column(db.Integer)
    
    numero = db.Column(db.String(50))
    articles = db.Column(db.JSON)
    
    sous_total = db.Column(db.Numeric, default=0)
    remise = db.Column(db.Numeric, default=0)
    type_remise = db.Column(db.String(20), default='pourcentage')
    valeur_remise = db.Column(db.Numeric, default=0)
    net_a_payer = db.Column(db.Numeric, default=0)
    tva_taux = db.Column(db.Numeric, default=18)
    
    medecin_prescripteur = db.Column(db.String(200))
    notes = db.Column(db.Text)
    rib = db.Column(db.String(100))
    numero_affiliation = db.Column(db.String(100))
    
    statut = db.Column(db.String(20), default='en_attente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100))


# ============================================================
# VENTES LUNETTES
# ============================================================
class VenteLunette(db.Model):
    __tablename__ = 'ventes_lunettes'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    patient_nom = db.Column(db.String(200))
    structure_id = db.Column(db.Integer, nullable=False)
    
    lunette_id = db.Column(db.Integer)
    lunette_nom = db.Column(db.String(200))
    marque = db.Column(db.String(100))
    modele = db.Column(db.String(100))
    
    prix = db.Column(db.Float, default=0)
    remise = db.Column(db.Float, default=0)
    prix_avec_remise = db.Column(db.Float, default=0)
    quantite = db.Column(db.Integer, default=1)
    total = db.Column(db.Float, default=0)
    
    taux_assurance = db.Column(db.Float, default=0)
    prise_en_charge = db.Column(db.Float, default=0)
    prise_en_charge2 = db.Column(db.Float, default=0)
    net_a_payer = db.Column(db.Float, default=0)
    
    mode_paiement = db.Column(db.String(50), default='especes')
    montant_donne = db.Column(db.Float, default=0)
    rendu = db.Column(db.Float, default=0)
    reste_a_payer = db.Column(db.Float, default=0)
    
    created_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================
# RECETTES
# ============================================================
class Recette(db.Model):
    __tablename__ = 'recettes'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Numeric, nullable=False)
    source = db.Column(db.String(100))
    source_id = db.Column(db.Integer)
    source_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    date_recette = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer)
    created_by_nom = db.Column(db.String(100))
    est_annulation = db.Column(db.Boolean, default=False)


# ============================================================
# DEPENSES
# ============================================================
class Depense(db.Model):
    __tablename__ = 'depenses'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Numeric, nullable=False)
    motif = db.Column(db.String(100), nullable=False)
    motif_personnalise = db.Column(db.String(200))
    description = db.Column(db.Text)
    piece_jointe = db.Column(db.String(500))
    date_depense = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer)
    created_by_nom = db.Column(db.String(100))


# ============================================================
# CAISSE
# ============================================================
class Caisse(db.Model):
    __tablename__ = 'caisse'
    
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, nullable=False)
    solde_actuel = db.Column(db.Numeric, default=0)
    solde_initial = db.Column(db.Numeric, default=0)
    date_mise_a_jour = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================
# ANNULATIONS VENTES
# ============================================================
class AnnulationVente(db.Model):
    __tablename__ = 'annulations_ventes'
    
    id = db.Column(db.Integer, primary_key=True)
    vente_id = db.Column(db.Integer, nullable=False)
    vente_type = db.Column(db.String(20))
    motif = db.Column(db.String(255))
    annule_par_id = db.Column(db.Integer)
    annule_par_nom = db.Column(db.String(100))
    ancien_net_a_payer = db.Column(db.Numeric)
    ancien_sous_total = db.Column(db.Numeric)
    data_avant = db.Column(db.JSON)
    date_annulation = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================
# RENDEZ-VOUS
# ============================================================
class RendezVous(db.Model):
    __tablename__ = 'rendez_vous'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    structure_id = db.Column(db.Integer, nullable=False)
    date_rdv = db.Column(db.Date, nullable=False)
    heure_rdv = db.Column(db.Time, nullable=False)
    motif = db.Column(db.String(200))
    statut = db.Column(db.String(20), default='programme')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rappel_envoye = db.Column(db.String(20), default='non')


# ============================================================
# PRESCRIPTIONS REÇUES
# ============================================================
class PrescriptionRecue(db.Model):
    __tablename__ = 'prescriptions_recues'
    
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer)
    structure_id = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer)
    patient_nom = db.Column(db.String(100))
    patient_prenom = db.Column(db.String(100))
    telephone = db.Column(db.String(50))
    
    # Médicament
    medicament = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(50))
    forme = db.Column(db.String(50))
    quantite = db.Column(db.String(50))
    duree_jours = db.Column(db.Integer)
    frequence = db.Column(db.String(100))
    instructions = db.Column(db.Text)
    
    # Type
    type_prescription = db.Column(db.String(20), default='medicament')
    date_prescription = db.Column(db.DateTime)
    prescripteur = db.Column(db.String(100))
    
    # Statut
    statut = db.Column(db.String(20), default='EN_ATTENTE')
    recu_le = db.Column(db.DateTime, default=datetime.utcnow)
    delivre_le = db.Column(db.DateTime)
    facture_le = db.Column(db.DateTime)
    
    # Prix
    prix_unitaire = db.Column(db.Numeric, default=0)
    prix_total = db.Column(db.Numeric, default=0)
    pbr = db.Column(db.Numeric, default=0)
    
    # Assurances
    type_assurance = db.Column(db.String(50))
    taux_prise_charge = db.Column(db.Numeric, default=0)
    numero_assure = db.Column(db.String(50))
    assurance2_nom = db.Column(db.String(100))
    taux_assurance2 = db.Column(db.Numeric, default=0)


# ============================================================
# STRUCTURE MAPPING
# ============================================================
class StructureMapping(db.Model):
    __tablename__ = 'structure_mappings'
    
    id = db.Column(db.Integer, primary_key=True)
    local_structure_id = db.Column(db.Integer, nullable=False)
    source_structure_id = db.Column(db.Integer, nullable=False)
    source_name = db.Column(db.String(50), default='ghp')
    api_url = db.Column(db.String(255))
    api_key = db.Column(db.String(255))
    last_sync = db.Column(db.DateTime)
    actif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)