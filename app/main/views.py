from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm

from ..compadre.forms import SpeciesForm, TaxonomyForm, TraitForm, PopulationForm, MatrixForm, PublicationForm, StudyForm, DeleteForm

from .. import db
from ..models import Permission, Role, User, \
                    IUCNStatus, ESAStatus, OrganismType, GrowthFormRaunkiaer, ReproductiveRepetition, \
                    DicotMonoc, AngioGymno, SpandExGrowthType, SourceType, Database, Purpose, MissingData, ContentEmail, Ecoregion, Continent, InvasiveStatusStudy, InvasiveStatusElsewhere, StageTypeClass, \
                    TransitionType, MatrixComposition, StartSeason, EndSeason, StudiedSex, Captivity, Species, Taxonomy, PurposeEndangered, PurposeWeed, Trait, \
                    Publication, Study, AuthorContact, AdditionalSource, Population, Stage, StageType, Treatment, \
                    MatrixStage, MatrixValue, Matrix, Interval, Fixed, Small, CensusTiming, Institute, Status, Version
from ..decorators import admin_required, permission_required, crossdomain


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
 
    return render_template('index.html')


@main.route('/meta-tables/')
# @login_required
def meta_tables_json():

    # Constructing dict for meta tables, ordering by main Class
    meta_tables = {"User" : {"Institute" : []},
                   "Species" : {"IUCNStatus" : [], "ESAStatus" : []}, "Taxonomy" : {}, "Trait" : {"OrganismType" : [], \
                   "GrowthFormRaunkiaer" : [], "ReproductiveRepetition" : [], "DicotMonoc" : [], "AngioGymno" : [], "SpandExGrowthType" : [] }, \
                   "Publication" : {"SourceType" : [], "Database" : [], "Purpose" : [], "MissingData" : [] }, \
                   "AuthorContact" : { "ContentEmail" : [] }, "Population" : {"Ecoregion" : [], "Continent" : [] , "InvasiveStatusStudy" : [], "InvasiveStatusElsewhere" : []}, \
                   "StageType" : { "StageTypeClass" : [] }, "MatrixValue" : { "TransitionType" : [] }, \
                   "Matrix" : {"MatrixComposition" : [], "StartSeason" : [], "EndSeason" : [], "StudiedSex" : [], "Captivity" : []}, \
                   "Fixed" : { "Small": [], "CensusTiming" : [] },
                   "Study" : { "PurposeEndangered": [], "PurposeWeed" : []}}

    meta_tables["User"]["Institute"].extend(Institute.query.all())
    meta_tables["Species"]["IUCNStatus"].extend(IUCNStatus.query.all())
    meta_tables["Species"]["ESAStatus"].extend(ESAStatus.query.all())
    meta_tables["Trait"]["OrganismType"].extend(OrganismType.query.all())
    meta_tables["Trait"]["GrowthFormRaunkiaer"].extend(GrowthFormRaunkiaer.query.all())
    meta_tables["Trait"]["ReproductiveRepetition"].extend(ReproductiveRepetition.query.all())
    meta_tables["Trait"]["DicotMonoc"].extend(DicotMonoc.query.all())
    meta_tables["Trait"]["AngioGymno"].extend(AngioGymno.query.all())
    meta_tables["Trait"]["SpandExGrowthType"].extend(SpandExGrowthType.query.all())
    meta_tables["Publication"]["SourceType"].extend(SourceType.query.all())
    meta_tables["Publication"]["Database"].extend(Database.query.all())
    meta_tables["Publication"]["Purpose"].extend(Purpose.query.all())
    meta_tables["Publication"]["MissingData"].extend(MissingData.query.all())
    meta_tables["AuthorContact"]["ContentEmail"].extend(ContentEmail.query.all())
    meta_tables["Population"]["Ecoregion"].extend(Ecoregion.query.all())
    meta_tables["Population"]["Continent"].extend(Continent.query.all())
    meta_tables["Population"]["InvasiveStatusStudy"].extend(InvasiveStatusStudy.query.all())
    meta_tables["Population"]["InvasiveStatusElsewhere"].extend(InvasiveStatusElsewhere.query.all())
    meta_tables["StageType"]["StageTypeClass"].extend(StageTypeClass.query.all())
    meta_tables["MatrixValue"]["TransitionType"].extend(TransitionType.query.all())
    meta_tables["Matrix"]["MatrixComposition"].extend(MatrixComposition.query.all())
    meta_tables["Matrix"]["StartSeason"].extend(StartSeason.query.all())
    meta_tables["Matrix"]["EndSeason"].extend(EndSeason.query.all())
    meta_tables["Matrix"]["StudiedSex"].extend(StudiedSex.query.all())
    meta_tables["Matrix"]["Captivity"].extend(Captivity.query.all())
    meta_tables["Fixed"]["Small"].extend(Small.query.all())
    meta_tables["Fixed"]["CensusTiming"].extend(CensusTiming.query.all())
    meta_tables["Study"]["PurposeEndangered"].extend(PurposeEndangered.query.all())
    meta_tables["Study"]["PurposeWeed"].extend(PurposeWeed.query.all())

    print meta_tables

    return render_template('meta.html', meta=meta_tables)

# now defunct 'display all data' page
@main.route('/data/')
# @login_required
def data():
    species = Species.query.all()

    return render_template('data.html', species=species)

### TABLE PAGES
# the big table of species
@main.route('/species-table/')
# @login_required
def species_table():
    # species = Species.query.all()
    species = Species.query.all()
    return render_template('species_table_template.html', species=species)

# the big table of publications
@main.route('/publications-table/')
# @login_required
def publications_table():
    publications = Publication.query.all()
    return render_template('publications_table_template.html', publications=publications)

###############################################################################################################################
### OVERVIEW PAGES
# species overview page
@main.route('/species/<int:id>/overview')
# @login_required
def species_page(id):
    species = Species.query.filter_by(id=id).first_or_404()
    return render_template('species_template.html',species = species)

# species overview TEST page
@main.route('/species/<int:id>/testoverview')
# @login_required
def species_page_test(id):
    species = Species.query.filter_by(id=id).first_or_404()
    taxonomy = Taxonomy.query.filter_by(id=species.id).first_or_404()
    trait = Trait.query.filter_by(id=species.id).first_or_404()
    populations = Population.query.filter_by(id=species.id)
    return render_template('species_template_test.html',species = species, taxonomy = taxonomy, trait = trait, populations = populations)

# publication overview page
@main.route('/publication/<int:id>')
# @login_required
def publication_page(id):
    publication = Publication.query.filter_by(id=id).first_or_404()
    return render_template('source_template.html',publication = publication)

# explorer
@main.route('/explorer/<taxon_level>/<taxon>')
# @login_required
def explorer(taxon_level,taxon):
    if taxon_level == "life":
        taxon_list = Taxonomy.query.all()
        next_taxon_level = "kingdom"
        tax_pos = 0
    elif taxon_level == "kingdom":
        taxon_list = Taxonomy.query.filter_by(kingdom=taxon)
        next_taxon_level = "phylum"
        tax_pos = 1
    elif taxon_level == "phylum":
        taxon_list = Taxonomy.query.filter_by(phylum=taxon)
        next_taxon_level = "class" 
        tax_pos = 2
    elif taxon_level == "class":
        taxon_list = Taxonomy.query.filter_by(tax_class=taxon)
        next_taxon_level = "order"
        tax_pos = 3
    elif taxon_level == "order":
        taxon_list = Taxonomy.query.filter_by(tax_order=taxon)
        next_taxon_level = "family"
        tax_pos = 4
    elif taxon_level == "family":
        taxon_list = Taxonomy.query.filter_by(family=taxon)
        next_taxon_level = "Species"
        tax_pos = 5
    
    
    return render_template('explorer_template.html',taxon=taxon,taxon_list = taxon_list,taxon_level=taxon_level,next_taxon_level=next_taxon_level, tax_pos = tax_pos)

# contribute
@main.route('/contribute-data')
def contribute_data():
    return render_template('contribute_data.html')

@main.route('/education')
def education():
    return render_template('about/education.html')

@main.route('/news')
def news():
    return render_template('about/news.html')

@main.route('/team')
def team():
    return render_template('about/team.html')

@main.route('/FAQs')
def FAQs():
    return render_template('about/FAQs.html')

@main.route('/history')
def history():
    return render_template('about/history.html')

@main.route('/funding')
def funding():
    return render_template('about/funding.html')

@main.route('/publications')
def publications():
    return render_template('about/publications.html')

###############################################################################################################################
### SPECIES/TAXONOMY/TRAIT FORMS + VIEW EDIT HISTORY PAGES

# editing species information #updated 25/1/17
@main.route('/species/<int:id>/edit', methods=['GET', 'POST'])
def species_form(id):
    species = Species.query.get_or_404(id)
    form = SpeciesForm(species=species)

    if form.validate_on_submit():
        species.species_accepted = form.species_accepted.data
        species.species_common = form.species_common.data
        species.iucn_status = form.iucn_status.data
        species.esa_status = form.esa_status.data
        species.species_gisd_status = form.species_gisd_status.data #
        species.species_iucn_taxonid = form.species_iucn_taxonid.data #
        species.species_iucn_population_assessed = form.species_iucn_population_assessed.data #
        species.invasive_status = form.invasive_status.data
        species.gbif_taxon_key = form.gbif_taxon_key.data
        species.image_path = form.image_path.data
        species.image_path2 = form.image_path2.data

        species.save_as_version()
        flash('The species infomation has been updated.')
        return redirect(url_for('.species_page',id=id))
    
    form.species_accepted.data = species.species_accepted
    form.species_common.data = species.species_common
    form.iucn_status.data = species.iucn_status
    form.esa_status.data = species.esa_status
    form.species_gisd_status.data = species.species_gisd_status #
    form.species_iucn_taxonid.data = species.species_iucn_taxonid #
    form.species_iucn_population_assessed.data = species.species_iucn_population_assessed #
    form.invasive_status.data = species.invasive_status
    form.gbif_taxon_key.data = species.gbif_taxon_key
    form.image_path.data = species.image_path
    form.image_path2.data = species.image_path2
    
    return render_template('data_entry/generic_form.html', form=form, species=species)

# species information edit history
@main.route('/species/<int:id>/edit-history')
def species_edit_history(id):
    species = Species.query.get_or_404(id)
    return render_template('edit_history.html', species=species)

# editing taxonomy # updated 25/1/17
@main.route('/taxonomy/<int:id>/edit', methods=['GET', 'POST'])
def taxonomy_form(id):
    taxonomy = Taxonomy.query.get_or_404(id)
    species = Species.query.get_or_404(taxonomy.species_id)
    form = TaxonomyForm(taxonomy=taxonomy)
    
    if form.validate_on_submit():
        taxonomy.authority = form.authority.data
        taxonomy.tpl_version = form.tpl_version.data
        taxonomy.infraspecies_accepted = form.infraspecies_accepted.data
        taxonomy.species_epithet_accepted = form.species_epithet_accepted.data 
        taxonomy.genus_accepted = form.genus_accepted.data
        taxonomy.genus = form.genus.data
        taxonomy.family = form.family.data
        taxonomy.tax_order = form.tax_order.data
        taxonomy.tax_class = form.tax_class.data
        taxonomy.phylum = form.phylum.data
        taxonomy.kingdom = form.kingdom.data
        taxonomy.col_check_ok = form.col_check_ok.data #
        taxonomy.col_check_date = form.col_check_date.data #
        
        flash('The taxonomy has been updated.')
        species_name = species.species_accepted
        return redirect(url_for('.species_page',id=species.id))
    
    form.authority.data = taxonomy.authority
    form.tpl_version.data = taxonomy.tpl_version
    form.infraspecies_accepted.data = taxonomy.infraspecies_accepted
    form.species_epithet_accepted.data = taxonomy.species_epithet_accepted
    form.genus_accepted.data = taxonomy.genus_accepted
    form.genus.data = taxonomy.genus
    form.family.data = taxonomy.family
    form.tax_order.data = taxonomy.tax_order
    form.tax_class.data = taxonomy.tax_class
    form.phylum.data = taxonomy.phylum
    form.kingdom.data = taxonomy.kingdom
    form.col_check_ok.data = taxonomy.col_check_ok
    form.col_check_date.data = taxonomy.col_check_date

    return render_template('data_entry/generic_form.html', form=form, taxonomy=taxonomy,species = species)

# taxonomy edit history
@main.route('/taxonomy/<int:id>/edit-history')
def taxonomy_edit_history(id):
    taxonomy = Taxonomy.query.get_or_404(id)
    return render_template('edit_history.html', taxonomy=taxonomy)

# editing traits
@main.route('/traits/<int:id>/edit', methods=['GET', 'POST'])
def trait_form(id):
    trait = Trait.query.get_or_404(id)
    species = Species.query.get_or_404(trait.species_id)
    form = TraitForm(trait=trait)
    
    if form.validate_on_submit():
        trait.max_height = form.max_height.data
        trait.organism_type = form.organism_type.data
        trait.growth_form_raunkiaer = form.growth_form_raunkiaer.data
        trait.reproductive_repetition = form.reproductive_repetition.data
        trait.dicot_monoc = form.dicot_monoc.data
        trait.angio_gymno = form.angio_gymno.data
        trait.spand_ex_growth_types = form.spand_ex_growth_types.data
        flash('The trait infomation has been updated.')
        return redirect(url_for('.species_page',id=species.id))
    
    form.max_height.data = trait.max_height
    form.organism_type.data = trait.organism_type
    form.growth_form_raunkiaer.data = trait.growth_form_raunkiaer
    form.reproductive_repetition.data = trait.reproductive_repetition
    form.dicot_monoc.data = trait.dicot_monoc
    form.angio_gymno.data = trait.angio_gymno
    form.spand_ex_growth_types.data = trait.spand_ex_growth_types
    return render_template('data_entry/generic_form.html', form=form, trait=trait,species = species)

# traits edit history
@main.route('/traits/<int:id>/edit-history')
def trait_edit_history(id):
    trait = Trait.query.get_or_404(id)
    return render_template('edit_history.html', trait=trait)

# editing publication
@main.route('/publication/<int:id>/edit', methods=['GET', 'POST'])
def publication_form(id):
    publication = Publication.query.get_or_404(id)
    form = PublicationForm()
    
    if form.validate_on_submit():
        publication.source_type = form.source_type.data
        publication.authors = form.authors.data 
        publication.editors = form.editors.data
        publication.pub_title = form.pub_title.data
        publication.journal_book_conf = form.journal_book_conf.data
        publication.year = form.year.data
        publication.volume = form.volume.data
        publication.pages = form.pages.data
        publication.publisher = form.publisher.data
        publication.city = form.city.data
        publication.country = form.country.data
        publication.institution = form.institution.data
        publication.DOI_ISBN = form.DOI_ISBN.data
        publication.name = form.pub_name.data
        publication.corresponding_author = form.corresponding_author.data
        publication.email = form.email.data
        publication.purposes_id = form.purposes.data
        publication.embargo = form.embargo.data
        publication.missing_data = form.missing_data.data
        publication.additional_source_string = form.additional_source_string.data   
        flash('The publication infomation has been updated.')
        return redirect(url_for('.publication_page',id=id))
    
    form.source_type.data = publication.source_type
    form.authors.data = publication.authors
    form.editors.data = publication.editors
    form.pub_title.data = publication.pub_title
    form.journal_book_conf.data = publication.journal_book_conf
    form.year.data = publication.year
    form.volume.data = publication.volume
    form.pages.data = publication.pages
    form.publisher.data = publication.publisher
    form.city.data = publication.city
    form.country.data = publication.country
    form.institution.data = publication.institution
    form.DOI_ISBN.data = publication.DOI_ISBN
    form.pub_name.data = publication.name
    form.corresponding_author.data = publication.corresponding_author
    form.email.data = publication.email
    form.purposes.data = publication.purposes_id
    form.embargo.data = publication.embargo
    form.missing_data.data = publication.missing_data
    form.additional_source_string.data = publication.additional_source_string
    
    
    return render_template('data_entry/publication_form.html', form=form, publication=publication)

# publication edit history
@main.route('/publication/<int:id>/edit-history')
def publication_edit_history(id):
    publication = Publication.query.get_or_404(id)
    return render_template('edit_history.html', publication=publication)

# editing population infomation
# COORDINATES NOT IMPLEMENTED
@main.route('/population/<int:id>/edit', methods=['GET', 'POST'])
def population_form(id):
    population = Population.query.get_or_404(id)
    species = Species.query.get_or_404(population.species_id)
    form = PopulationForm(population=population)
    
    if form.validate_on_submit():
        population.name = form.name.data
        population.ecoregion = form.ecoregion.data
        population.country = form.country.data
        population.continent = form.continent.data
        population.latitude = form.latitude.data
        population.longitude = form.longitude.data
        population.altitude = form.altitude.data
        flash('The population infomation has been updated.')
        return redirect(url_for('.species_page',id=species.id))
        
    form.name.data = population.name
    form.ecoregion.data = population.ecoregion
    form.country.data = population.country
    form.continent.data = population.continent
    form.latitude.data = population.latitude
    form.longitude.data = population.longitude
    form.altitude.data = population.altitude
    
    return render_template('data_entry/generic_form.html', form=form, population=population,species = species)

# population edit history
@main.route('/population/<int:id>/edit-history')
def population_edit_history(id):
    population = Population.query.get_or_404(id)
    return render_template('edit_history.html', population=population)

# edting study infomation
@main.route('/study/<int:id>/edit', methods=['GET', 'POST'])
def study_form(id):
    study = Study.query.get_or_404(id)
    publication = study.publication_id
    form = StudyForm(study=study)
    
    if form.validate_on_submit():
        study.study_duration = form.study_duration.data
        study.study_start = form.study_start.data
        study.study_end = form.study_end.data
        flash('The study infomation has been updated.')
        return redirect(url_for('.publication_page',id=species.id))
        
    form.study_duration.data = study.study_duration
    form.study_start.data = study.study_start
    form.study_end.data = study.study_end
    
    return render_template('data_entry/generic_form.html', form=form, study=study)

# study edit history
@main.route('/study/<int:id>/edit-history')
def study_edit_history(id):
    study = Study.query.get_or_404(id)
    return render_template('edit_history.html', study=study)

# editing matrix 
@main.route('/matrix/<int:id>/edit', methods=['GET', 'POST'])
def matrix_form(id):
    matrix = Matrix.query.get_or_404(id)
    population = Population.query.get_or_404(matrix.population_id)
    species = Species.query.get_or_404(population.species_id)
    form = MatrixForm(matrix=matrix)
    
    if form.validate_on_submit():
        matrix.treatment = form.treatment.data
        matrix.matrix_split = form.matrix_split.data
        matrix.matrix_composition = form.matrix_composition.data
        matrix.survival_issue = form.survival_issue.data
        matrix.n_intervals = form.n_intervals.data
        matrix.periodicity = form.periodicity.data
        matrix.matrix_criteria_size = form.matrix_criteria_size.data
        matrix.matrix_criteria_ontogeny = form.matrix_criteria_ontogeny.data
        matrix.matrix_criteria_age = form.matrix_criteria_age.data
        matrix.matrix_start = form.matrix_start.data
        matrix.matrix_end = form.matrix_end.data
        matrix.matrix_start_season_id = form.matrix_start_season_id.data
        matrix.matrix_end_season_id = form.matrix_end_season_id.data
        matrix.matrix_fec = form.matrix_fec.data
        matrix.matrix_a_string = form.matrix_a_string.data
        matrix.matrix_u_string = form.matrix_u_string.data
        matrix.matrix_f_string = form.matrix_f_string.data
        matrix.matrix_c_string = form.matrix_c_string.data
        matrix.matrix_class_string = form.matrix_class_string.data
        matrix.n_plots = form.n_plots.data
        matrix.plot_size = form.plot_size.data
        matrix.n_individuals = form.n_individuals.data
        matrix.studied_sex = form.studied_sex.data
        matrix.captivity_id = form.captivity_id.data
        matrix.matrix_dimension = form.matrix_dimension.data
        matrix.observations = form.observations.data
        flash('The matrix infomation has been updated.')
        return redirect(url_for('.species_page',id=species.id))
        
    form.treatment.data = matrix.treatment.treatment_name
    form.matrix_split.data = matrix.matrix_split
    form.matrix_composition.data = matrix.matrix_composition
    form.survival_issue.data = matrix.survival_issue
    form.n_intervals.data = matrix.n_intervals
    form.periodicity.data = matrix.periodicity
    form.matrix_criteria_size.data = matrix.matrix_criteria_size
    form.matrix_criteria_ontogeny.data = matrix.matrix_criteria_ontogeny
    form.matrix_criteria_age.data = matrix.matrix_criteria_age
    form.matrix_start.data = matrix.matrix_start
    form.matrix_end.data = matrix.matrix_end 
    form.matrix_start_season_id.data = matrix.matrix_start_season_id
    form.matrix_end_season_id.data = matrix.matrix_end_season_id 
    form.matrix_fec.data = matrix.matrix_fec
    form.matrix_dimension.data = matrix.matrix_dimension
    form.matrix_a_string.data = matrix.matrix_a_string
    form.matrix_u_string.data = matrix.matrix_u_string
    form.matrix_f_string.data = matrix.matrix_f_string
    form.matrix_c_string.data = matrix.matrix_c_string
    form.matrix_class_string.data = matrix.matrix_class_string
    form.n_plots.data = matrix.n_plots
    form.plot_size.data = matrix.plot_size 
    form.n_individuals.data = matrix.n_individuals
    form.studied_sex.data = matrix.studied_sex
    form.captivity_id.data = matrix.captivity_id
    form.observations.data = matrix.observations
    
    return render_template('data_entry/matrix_form.html', form=form, matrix=matrix,population=population,species = species)

# matrix edit history
@main.route('/matrix/<int:id>/edit-history')
def matrix_edit_history(id):
    matrix = Matrix.query.get_or_404(id)
    return render_template('edit_history.html', matrix= matrix)

### END OF EDITING FORMS + EDIT HISTORY

###############################################################################################################################
### NEW DATA INPUT FORMS

@main.route('/species/new', methods=['GET', 'POST'])
def species_new_form():
    form = SpeciesForm()
    if form.validate_on_submit():
        species = Species()
        
        species.species_accepted = form.species_accepted.data
        species.species_common = form.species_common.data
        species.iucn_status = form.iucn_status.data
        species.esa_status = form.esa_status.data
        species.invasive_status = form.invasive_status.data
        species.gbif_taxon_key = form.gbif_taxon_key.data
        species.image_path = form.image_path.data
        species.image_path2 = form.image_path2.data
        
        db.session.add(species)
        db.session.commit()

        return redirect(url_for('.species_page',id=species.id))
    
    return render_template('data_entry/generic_form.html', form=form)

@main.route('/taxonomy/new/species=<int:id_sp>', methods=['GET', 'POST'])
def taxonomy_new_form(id_sp):
    species = Species.query.get_or_404(id_sp)
    form = TaxonomyForm()
    
    if form.validate_on_submit():
        taxonomy = Taxonomy()
        taxonomy.species_id = species.id
        taxonomy.species_author = form.species_author.data
        taxonomy.authority = form.authority.data
        taxonomy.taxonomic_status = form.taxonomic_status.data
        taxonomy.tpl_version = form.tpl_version.data
        taxonomy.infraspecies_accepted = form.infraspecies_accepted.data
        taxonomy.species_epithet_accepted = form.species_epithet_accepted.data 
        taxonomy.genus_accepted = form.genus_accepted.data
        taxonomy.genus = form.genus.data
        taxonomy.family = form.family.data
        taxonomy.tax_order = form.tax_order.data
        taxonomy.tax_class = form.tax_class.data
        taxonomy.phylum = form.phylum.data
        taxonomy.kingdom = form.kingdom.data
        
        db.session.add(taxonomy)
        db.session.commit()
        
        return redirect(url_for('.species_page',id=id_sp))
    
    return render_template('data_entry/generic_form.html', form=form,species = species)

@main.route('/traits/new/species=<int:id_sp>', methods=['GET', 'POST'])
def trait_new_form(id_sp):
    species = Species.query.get_or_404(id_sp)
    form = TraitForm()
    
    if form.validate_on_submit():
        Trait = Trait()
        trait.species_id = species.id
        
        trait.max_height = form.max_height.data
        trait.organism_type = form.organism_type.data
        trait.growth_form_raunkiaer = form.growth_form_raunkiaer.data
        trait.reproductive_repetition = form.reproductive_repetition.data
        trait.dicot_monoc = form.dicot_monoc.data
        trait.angio_gymno = form.angio_gymno.data
        return redirect(url_for('.species_page',id=id_sp))
    
    return render_template('data_entry/generic_form.html', form=form,species = species)

@main.route('/publication/new', methods=['GET', 'POST'])
def new_publication_form():
    form = PublicationForm()
    
    if form.validate_on_submit():
        publication = Publication()
        
        publication.source_type = form.source_type.data
        publication.authors = form.authors.data 
        publication.editors = form.editors.data
        publication.pub_title = form.pub_title.data
        publication.journal_book_conf = form.journal_book_conf.data
        publication.year = form.year.data
        publication.volume = form.volume.data
        publication.pages = form.pages.data
        publication.publisher = form.publisher.data
        publication.city = form.city.data
        publication.country = form.country.data
        publication.institution = form.institution.data
        publication.DOI_ISBN = form.DOI_ISBN.data
        publication.name = form.pub_name.data
        publication.corresponding_author = form.corresponding_author.data
        publication.email = form.email.data
        publication.purposes_id = form.purposes.data
        publication.embargo = form.embargo.data
        publication.missing_data = form.missing_data.data
        publication.additional_source_string = form.additional_source_string.data  
        
        db.session.add(publication)
        db.session.commit()
        
        return redirect(url_for('.publication_page',id=publication.id))
    
    return render_template('data_entry/publication_form.html',form=form)

@main.route('/population/new/publication=<int:id_pub>/choose_species', methods=['GET'])
def choose_species(id_pub):
    publication = Publication.query.get_or_404(id_pub)
    species = Species.query.all()
    
    return render_template('data_entry/choose_species.html',publication=publication,species=species)
    
@main.route('/population/new/publication=<int:id_pub>/species=<int:id_sp>', methods=['GET', 'POST'])
def population_new_form(id_pub,id_sp):
    publication = Publication.query.get_or_404(id_pub)
    species = Species.query.get_or_404(id_sp)
    form = PopulationForm()
    
    if form.validate_on_submit():
        population = Population()
        population.publication_id = id_pub
        population.species_id = id_sp
        
        population.name = form.name.data
        population.ecoregion = form.ecoregion.data
        population.country = form.country.data
        population.continent = form.continent.data
        population.latitude = form.latitude.data
        population.longitude = form.longitude.data
        population.altitude = form.altitude.data
        
        db.session.add(population)
        db.session.commit()
        
        return redirect(url_for('.publication_page',id=id_pub))
    
    return render_template('data_entry/generic_form.html', form=form, publication=publication, species=species)


### END OF NEW DATA FORMS

###############################################################################################################################
### Delete stuff

@main.route('/delete/<thing_to_delete>/<int:id_obj>', methods=['GET', 'POST'])
def delete_object(thing_to_delete,id_obj):
    form = DeleteForm()
    
    if thing_to_delete == "population":
        population = Population.query.get_or_404(id_obj)
        
    if thing_to_delete == "species":
        species = Species.query.get_or_404(id_obj)
        populations = Population.query.filter_by(species_id=id_obj)
        taxonomy = Taxonomy(species_id=id_obj)
        traits = Traits(species_id=id_obj)
    
    if thing_to_delete == "publication":
        publication = Publication.query.get_or_404(id_obj)
        populations = Population.query.filter_by(publication_id=id_obj)
        
    if thing_to_delete == "matrix":
        matrix = Matrix.query.get_or_404(id_obj)
        
        
    if form.validate_on_submit() and thing_to_delete == "population":
        db.session.delete(population)
        db.session.commit()
        flash('The population has been deleted')
        return redirect(url_for('.publication_page',id=population.publication_id))
    
    if form.validate_on_submit() and thing_to_delete == "species":
        db.session.delete(species)
        for p in populations:
            db.session.delete(p)
        db.session.commit()
        flash('The species has been deleted')
        return redirect(url_for('.species_table'))
    
    if form.validate_on_submit() and thing_to_delete == "publication":
        db.session.delete(publication)
        for p in populations:
            db.session.delete(p)
        db.session.commit()
        flash('The publication has been deleted')
        return redirect(url_for('.publications_table'))
    
    if form.validate_on_submit() and thing_to_delete == "matrix":
        db.session.delete(matrix)
        db.session.commit()
        flash('The matrix has been deleted')
        return redirect(url_for('.publication_page',id=matrix.publication_id))
    
    return render_template('data_entry/delete_confirm.html', form=form)

# USER + PROFILE PAGES
# User
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()    
    return render_template('user.html', user=user)

# edit profile
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

# edit a different profile as admin
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
