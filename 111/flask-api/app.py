from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy import ForeignKey, create_engine, Column, Text, CHAR, VARCHAR, Date, Integer, String, SmallInteger, Numeric, Unicode, UnicodeText
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import join
# import pymysql
# pymysql.install_as_MySQLdb()
from configdb import encoded_username, encoded_password

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://sandbox1.rssda.su"}})
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{encoded_username}:{encoded_password}@185.84.108.3/b187324_stamps'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<u187324_GN>:<3281#Db-77>@<185.84.108.3>/<b187324_stamps>'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/stamp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/amph_stamp_db'в докере
db = SQLAlchemy(app)
ma = Marshmallow(app)
class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.SmallInteger, primary_key=True)
    site_name = db.Column(db.VARCHAR(150), nullable=False)
    site_latitude = db.Column(db.Numeric (precision=7, scale=5))
    site_longitude = db.Column(db.Numeric (precision=7, scale=5))

    # def __init__(self, id, name, latitude, longitude):
    #     self.id = id
    #     self.name = name
    #     self.latitude = latitude
    #     self.longitude = longitude

class SiteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'site_name', 'site_latitude', 'site_longitude')

site_schema = SiteSchema()
sites_schema = SiteSchema(many=True)




class Manufact(db.Model):
    __tablename__ = 'manufact'
    id = db.Column(db.SmallInteger, primary_key=True)
    manufact_center = db.Column(db.VARCHAR(150), nullable=False)
    manufact_latitude = db.Column(db.Numeric (precision=7, scale=5))
    manufact_longitude = db.Column(db.Numeric (precision=7, scale=5))

class ManufactSchema(ma.Schema):
    class Meta:
        fields = ('id', 'manufact_center', 'manufact_latitude', 'manufact_longitude')

manufact_schema = ManufactSchema()
manufacts_schema = ManufactSchema(many=True)




class Artifact(db.Model):
    __tablename__ = 'artifact'
    id = db.Column(db.SmallInteger, primary_key=True)
    site_id = db.Column(db.SmallInteger, db.ForeignKey('site.id'))
    manufact_id = db.Column(db.SmallInteger, db.ForeignKey('manufact.id'))
    year_exc = db.Column(db.CHAR(4))
    unit_exc = db.Column(db.VARCHAR(150))
    leader_exc = db.Column(db.VARCHAR(150))
    artif_position = db.Column(db.VARCHAR(15))
    field_id = db.Column(db.VARCHAR(40), unique=True)
    artif_depository = db.Column(db.VARCHAR(40))
    depository_id = db.Column(db.VARCHAR(40), unique=True)
    description =  db.Column(db.Text)
    artif_g = db.Column(db.VARCHAR(15))
    artif_preservation = db.Column(db.VARCHAR(15))
    munsell_hue = db.Column(db.VARCHAR(7))
    munsell_value = db.Column(db.VARCHAR(2))
    munsell_chroma = db.Column(db.VARCHAR(2))
    munsell_code = db.Column(db.VARCHAR (10))
    munsell_name = db.Column(db.VARCHAR (30))

class ArtifactSchema(ma.Schema):
    class Meta:
        fields = ('id', 'site_id', 'manufact_id', 'year_exc', 'unit_exc', 'leader_exc', 'artif_position', 'field_id',
                  'artif_depository', 'depository_id', 'description', 'artif_g', 'artif_preservation', 'munsell_hue', 
                  'munsell_value', 'munsell_chroma', 'munsell_code', 'munsell_name')

artifact_schema = ArtifactSchema()
artifacts_schema = ArtifactSchema(many=True)




class Stamp(db.Model):
    __tablename__ = 'stamp'
    id = db.Column(db.CHAR(6), primary_key=True)
    artifact_id = db.Column(db.SmallInteger, db.ForeignKey('artifact.id'))
    stamp_position = db.Column(db.VARCHAR(10))
    stamp_preservation = db.Column(db.VARCHAR(10))
    stamp_preservation_comm = db.Column(db.VARCHAR(40))
    relief_type = db.Column(db.VARCHAR(20))
    content_type = db.Column(db.VARCHAR(20))
    shape_type = db.Column(db.VARCHAR(40))
    axis_large = db.Column(db.SmallInteger)
    axis_small = db.Column(db.SmallInteger)
    origin_type = db.Column(db.VARCHAR(15))
    magist_name = db.Column(db.VARCHAR(30))
    fabric_name = db.Column(db.VARCHAR(30))
    stamp_legend = db.Column(db.Text)
    stamp_legend_comment = db.Column(db.VARCHAR(500))
    emblem = db.Column(db.VARCHAR(200))
    date_text = db.Column(db.VARCHAR(50))
    date_early = db.Column(db.SmallInteger)
    date_late = db.Column(db.SmallInteger)
    finkelstein = db.Column(db.VARCHAR(20))
    garlan = db.Column(db.VARCHAR(20))
    xlink300px = db.Column(db.VARCHAR(80))
    xlink1000px = db.Column(db.VARCHAR(80))
    zlink300px = db.Column(db.VARCHAR(80))
    zlink1000px = db.Column(db.VARCHAR(80))
    glink300px = db.Column(db.VARCHAR(80))
    glink1000px = db.Column(db.VARCHAR(80))
    stamp_comments = db.Column(db.Text)
    published = db.Column(db.VARCHAR(100))

class StampSchema(ma.Schema):
    class Meta:
        fields = ('date_early', 'date_late', 'axis_large', 'axis_small', 'artifact_id', 'id', 'shape_type',
                   'origin_type', 'magist_name', 'fabric_name', 'stamp_legend', 'stamp_legend_comment',
                     'emblem', 'date_text', 'finkelstein', 'garlan', 'stamp_comments', 'stamp_position',
                       'stamp_preservation', 'stamp_preservation_comm', 'xlink300px', 'xlink1000px', 'zlink300px',
                        'zlink1000px', 'glink300px','glink1000px', 'relief_type', 'content_type')

stamp_schema = StampSchema()
stamps_schema = StampSchema(many=True)




class Model_3d(db.Model):
    __tablename__ = 'model_3d'
    model_id = db.Column(db.SmallInteger, primary_key=True)
    stamp_id = db.Column(db.SmallInteger, db.ForeignKey('stamp.id'))
    polygon_count = db.Column(db.Integer)
    polygon_sm = db.Column(db.Integer)
    polygon_size = db.Column(db.Integer)
    model_process = db.Column(db.VARCHAR(30))
    frame_count = db.Column(db.Integer)
    camera = db.Column(db.VARCHAR(40))
    lens = db.Column(db.VARCHAR(40))
    model_date = db.Column(db.Date)
    model_link = db.Column(db.VARCHAR(50))

class Model_3dSchema(ma.Schema):
    class Meta:
        fields = ('model_id', 'stamp_id', 'polygon_count', 'polygon_sm', 'polygon_size', 'model_process',
                  'frame_count', 'camera', 'lens', 'model_date', 'model_link')

model_3d_schema = Model_3dSchema()
models_3d_schema = Model_3dSchema(many=True)


# class Image(db.Model):
#     __tablename__ = 'image'
#     image_id = db.Column(db.SmallInteger, primary_key=True)
#     stamp_id = db.Column(db.SmallInteger, db.ForeignKey('stamp.id'))
#     image_type = db.Column(db.VARCHAR(40))
#     image_description = db.Column(db.Text ())
#     link300px = db.Column(db.VARCHAR(80))
#     link1000px = db.Column(db.VARCHAR(80))

# class ImageSchema(ma.Schema):
#     class Meta:
#         fields = ('image_id', 'stamp_id', 'image_type', 'image_description', 'link300px', 'link1000px')

# image_schema = ImageSchema()
# images_schema = ImageSchema(many=True)

    # // year_exc, artif_position(location), artif_g(groups), munsell_name
@app.route('/get_years', methods=['GET'])
def get_years():
    years = db.session.query(Artifact.year_exc).distinct().group_by(Artifact.year_exc).order_by(Artifact.year_exc.desc()).all()
    year_list = [int(year[0]) for year in years if year[0] is not None]
    return jsonify(year_list)

# @app.route('/get_years', methods=['GET'])
# def get_years():
#     years = Artifact.query.distinct(Artifact.year_exc).order_by(Artifact.year_exc.desc()).all()
#     year_list = [int(year.year_exc) for year in years if year.year_exc is not None]
#     return jsonify(year_list)

@app.route('/get_locations', methods=['GET'])
def get_locations():
    locations = Artifact.query.with_entities(Artifact.artif_position.distinct()).all()
    location_list = [location[0] for location in locations if location[0] is not None]
    return jsonify(location_list)

@app.route('/get_groups', methods=['GET'])
def get_groups():
    groups = Artifact.query.with_entities(Artifact.artif_g.distinct()).all()
    group_list = [group[0] for group in groups if group[0] is not None]
    return jsonify(group_list)

@app.route('/get_colors', methods=['GET'])
def get_colors():
    colors = Artifact.query.with_entities(Artifact.munsell_name.distinct()).all()
    color_list = [color[0] for color in colors if color[0] is not None]
    return jsonify(color_list)
    # // stamp_position, stamp_preservation, relief_type, content_type, shape_type, origin_type
@app.route('/get_positions', methods=['GET'])
def get_positions():
    positions = Stamp.query.with_entities(Stamp.stamp_position.distinct()).all()
    position_list = [position[0] for position in positions if position[0] is not None]
    return jsonify(position_list)

@app.route('/get_preservations', methods=['GET'])
def get_preservations():
    preservations = Stamp.query.with_entities(Stamp.stamp_preservation.distinct()).all()
    preservation_list = [preservation[0] for preservation in preservations if preservation[0] is not None]
    return jsonify(preservation_list)

@app.route('/get_reliefs', methods=['GET'])
def get_reliefs():
    reliefs = Stamp.query.with_entities(Stamp.relief_type.distinct()).all()
    relief_list = [relief[0] for relief in reliefs if relief[0] is not None]
    return jsonify(relief_list)

@app.route('/get_contents', methods=['GET'])
def get_contents():
    contents = Stamp.query.with_entities(Stamp.content_type.distinct()).all()
    content_list = [content[0] for content in contents if content[0] is not None]
    return jsonify(content_list)

@app.route('/get_shapes', methods=['GET'])
def get_shapes():
    shapes = Stamp.query.with_entities(Stamp.shape_type.distinct()).all()
    shape_list = [shape[0] for shape in shapes if shape[0] is not None]
    return jsonify(shape_list)

@app.route('/get_origins', methods=['GET'])
def get_origins():
    origins = Stamp.query.with_entities(Stamp.origin_type.distinct()).all()
    origin_list = [origin[0] for origin in origins if origin[0] is not None]
    return jsonify(origin_list)
# // date_early, date_late, finkelstein, garlan, emblem??? axis_small??, axis_large??
@app.route('/get_earlys', methods=['GET'])
def get_earlys():
    earlys = Stamp.query.with_entities(Stamp.date_early.distinct()).all()
    early_list = [early[0] for early in earlys if early[0] is not None]
    return jsonify(early_list)

@app.route('/get_lates', methods=['GET'])
def get_lates():
    lates = Stamp.query.with_entities(Stamp.date_late.distinct()).all()
    late_list = [late[0] for late in lates if late[0] is not None]
    return jsonify(late_list)

@app.route('/get_fis', methods=['GET'])
def get_fis():
    fis = Stamp.query.with_entities(Stamp.finkelstein.distinct()).all()
    fi_list = [fi[0] for fi in fis if fi[0] is not None]
    return jsonify(fi_list)

@app.route('/get_garlans', methods=['GET'])
def get_finkelsteins():
    garlans = Stamp.query.with_entities(Stamp.garlan.distinct()).all()
    garlan_list = [garlan[0] for garlan in garlans if garlan[0] is not None]
    return jsonify(garlan_list)






@app.route('/get_all', methods=['GET'])
def get_all():
    site_id = request.args.get('site_id')
    manufact_id = request.args.get('manufact_id')
    stamp_legend = request.args.get('stamp_legend')
    year_exc = request.args.get('year_exc')
    artif_position = request.args.get('artif_position')
    artif_g = request.args.get('artif_g')
    munsell_name = request.args.get('munsell_name')
    stamp_position = request.args.get('stamp_position')
    stamp_preservation = request.args.get('stamp_preservation')
    relief_type = request.args.get('relief_type')
    content_type = request.args.get('content_type')
    shape_type = request.args.get('shape_type')
    origin_type = request.args.get('origin_type')
    date_early = request.args.get('date_early')
    date_late = request.args.get('date_late')
    finkelstein = request.args.get('finkelstein')
    garlan = request.args.get('garlan')
    # // emblem axis_small??, axis_large??

    query = db.session.query(Site, Manufact, Artifact, Stamp, Model_3d).\
            filter(Site.id == Artifact.site_id).\
            filter(Manufact.id == Artifact.manufact_id).\
            filter(Artifact.id == Stamp.artifact_id).\
            filter(Stamp.id == Model_3d.stamp_id)
    
    if stamp_legend is not None:  # add this block to filter by stamp_legend
        query = query.filter(Stamp.stamp_legend.ilike(f"%{stamp_legend}%"))

    if site_id is not None:
        query = query.filter(Site.id == site_id)

    if manufact_id is not None:
        query = query.filter(Manufact.id == manufact_id)
    
    if year_exc is not None:   # add this check to filter by year_ex
        query = query.filter(Artifact.year_exc == year_exc)

    if artif_position is not None:
        query = query.filter(Artifact.artif_position == artif_position)

    if artif_g is not None:
        query = query.filter(Artifact.artif_g == artif_g)

    if munsell_name is not None:
        query = query.filter(Artifact.munsell_name == munsell_name)
    # // stamp_position, stamp_preservation, relief_type, content_type, shape_type, origin_type
    # // date_early, date_late, finkelstein, garlan, emblem??? axis_small??, axis_large??
    if stamp_position is not None:
        query = query.filter(Stamp.stamp_position == stamp_position)
    
    if stamp_preservation is not None:
        query = query.filter(Stamp.stamp_preservation == stamp_preservation)
    
    if relief_type is not None:
        query = query.filter(Stamp.relief_type == relief_type)

    if content_type is not None:
        query = query.filter(Stamp.content_type == content_type)
    
    if shape_type is not None:
        query = query.filter(Stamp.shape_type == shape_type)

    if origin_type is not None:
        query = query.filter(Stamp.origin_type == origin_type)
    
    if date_early is not None:
        query = query.filter(Stamp.date_early == date_early)

    if date_late is not None:
        query = query.filter(Stamp.date_late == date_late)

    if finkelstein is not None:
        query = query.filter(Stamp.finkelstein == finkelstein)

    if garlan is not None:
        query = query.filter(Stamp.garlan == garlan)

    joined_tables = query.all()

    results = []

    for site, manufact, artifact, stamp, model_3d in joined_tables:
        site_data = site_schema.dump(site)
        manufact_data = manufact_schema.dump(manufact)
        artifact_data = artifact_schema.dump(artifact)
        stamp_data = stamp_schema.dump(stamp)
        model_3d_data = model_3d_schema.dump(model_3d)

        data = {**site_data, **manufact_data, **artifact_data, **stamp_data, **model_3d_data}
        results.append(data)

    return jsonify(results)

@app.route('/get_item/<int:id>', methods=['GET'])
def get_item(id):
    joined_tables = db.session.query(Site, Manufact, Artifact, Stamp, Model_3d).filter(
        Site.id == Artifact.site_id,
        Manufact.id == Artifact.manufact_id,
        Artifact.id == Stamp.artifact_id,
        Stamp.id == Model_3d.stamp_id,
        Stamp.id == id  # filter by id
    ).all()

    if not joined_tables:
        return jsonify({'message': 'Item not found'}), 404
    
    site, manufact, artifact, stamp, model_3d = joined_tables[0]

    site_data = site_schema.dump(site)
    manufact_data = manufact_schema.dump(manufact)
    artifact_data = artifact_schema.dump(artifact)
    stamp_data = stamp_schema.dump(stamp)
    model_3d_data = model_3d_schema.dump(model_3d)

    data = {**site_data, **manufact_data, **artifact_data, **stamp_data, **model_3d_data}

    return jsonify(data)


@app.route('/get_sites', methods = ['GET'])
def get_sites():
    all_sites = Site.query.all()
    results = sites_schema.dump(all_sites)
    return jsonify(results)

@app.route('/get_sites/<id>/', methods = ['GET'])
def get_ditailes_site(id):
    site = Site.query.get(id)
    return site_schema.jsonify(site)



@app.route('/get_manufacts', methods = ['GET'])
def get_manufacts():
    all_manufacts = Manufact.query.all()
    results = manufacts_schema.dump(all_manufacts)
    return jsonify(results)

@app.route('/get_manufacts/<id>/', methods = ['GET'])
def get_ditailes_manufact(id):
    manufact = Manufact.query.get(id)
    return manufact_schema.jsonify(manufact)

@app.route('/get_models', methods = ['GET'])
def get_models():
    all_models = Model_3d.query.all()
    results = models_3d_schema.dump(all_models)
    return jsonify(results)

@app.route('/get_model/<model_id>/', methods = ['GET'])
def get_model(model_id):
    model = Model_3d.query.get(model_id)
    return model_3d_schema.jsonify(model)

if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)



# @app.route('/get_artifacts', methods = ['GET'])
# def get_artifacts():
#     all_artifacts = Artifact.query.all()
#     results = artifacts_schema.dump(all_artifacts)
#     return jsonify(results)

# @app.route('/get_artifacts/<id>/', methods = ['GET'])
# def get_ditailes_artifacts(id):
#     artifact = Artifact.query.get(id)
#     return artifact_schema.jsonify(artifact)



# @app.route('/get_stamps', methods = ['GET'])
# def get_stamps():
#     all_stamps = Stamp.query.all()
#     results = stamps_schema.dump(all_stamps)
#     return jsonify(results)

# @app.route('/get_stamps/<id>/', methods = ['GET'])
# def get_ditailes_stamps(id):
#     stamp = Stamp.query.get(id)
#     return stamp_schema.jsonify(stamp)


# @app.route('/get_images', methods = ['GET'])
# def get_images():
#     all_images = Image.query.all()
#     results = images_schema.dump(all_images)
#     return jsonify(results)

# @app.route('/get_images/<image_id>/', methods = ['GET'])
# def get_ditailes_images(image_id):
#     image = Image.query.get(image_id)
#     return image_schema.jsonify(image)

# @app.route('/get_stamps')
# def get_stamps():
#     query = db.session.query(
#         Stamp.id,
#         Artifact.id.label('artifact_id'),
#         Site.id.label('site_id'),
#         Manufact.id.label('manufact_id'),
#         Stamp.date_early,
#         Stamp.date_late,
#         Stamp.axis_large,
#         Stamp.axis_small,
#         Stamp.shape_type,
#         Stamp.origin_type,
#         Stamp.magist_name,
#         Stamp.fabric_name,
#         Stamp.stamp_legend,
#         Stamp.stamp_legend_comment,
#         Stamp.emblem,
#         Stamp.date_text,
#         Stamp.finkelstein,
#         Stamp.garlan,
#         Stamp.stamp_comments,
#         Stamp.stamp_position,
#         Stamp.stamp_preservation,
#         Stamp.stamp_preservation_comm,
#         Stamp.relief_type,
#         Stamp.content_type,
#         Model_3d.model_id,
#         Model_3d.polygon_count,
#         Model_3d.polygon_sm,
#         Model_3d.polygon_size,
#         Model_3d.model_process,
#         Model_3d.frame_count,
#         Model_3d.camera,
#         Model_3d.lens,
#         Model_3d.model_date,
#         Model_3d.model_link,
#         Image.image_id,
#         Image.image_type,
#         Image.image_description,
#         Image.link300px,
#         Image.link1000px
#     ).select_from(
#         join(
#             Stamp,
#             Artifact,
#             Site,
#             Manufact,
#             Model_3d,
#             Image,
#             Stamp.artifact_id == Artifact.id,
#             Artifact.site_id == Site.id,
#             Artifact.manufact_id == Manufact.id,
#             Stamp.id == Model_3d.stamp_id,
#             Stamp.id == Image.stamp_id,
#             isouter=True
#         )
#     )
#     stamps = query.all()
#     stamp_data = []
#     for stamp in stamps:
#         stamp_dict = {
#             'id': stamp.id,
#             'artifact_id': stamp.artifact_id,
#             'site_id': stamp.site_id,
#             'manufact_id': stamp.manufact_id,
#             'date_early': stamp.date_early,
#             'date_late': stamp.date_late,
#             'axis_large': stamp.axis_large,
#             'axis_small': stamp.axis_small,
#             'shape_type': stamp.shape_type,
#             'origin_type': stamp.origin_type,
#             'magist_name': stamp.magist_name,
#             'fabric_name': stamp.fabric_name,
#             'stamp_legend': stamp.stamp_legend,
#             'stamp_legend_comment': stamp.stamp_legend_comment,
#             'emblem': stamp.emblem,
#             'date_text': stamp.date_text,
#             'finkelstein': stamp.finkelstein,
#             'garlan': stamp.garlan,
#             'stamp_comments': stamp.stamp_comments,
#             'stamp_position': stamp.stamp_position,
#             'stamp_preservation': stamp.stamp_preservation,
#             'stamp_preservation_comm': stamp.stamp_preservation_comm,
#             'relief_type': stamp.relief_type,
#             'content_type': stamp.content_type,
#             'model_id': stamp.model_id,
#             'polygon_count': stamp.polygon_count,
#             'polygon_sm': stamp.polygon_sm,
#             'polygon_size': stamp.polygon_size,
#             'model_process': stamp.model_process,
#             'frame_count': stamp.frame_count,
#             'camera': stamp.camera,
#             'lens': stamp.lens,
#             'model_date': stamp.model_date,
#             'model_link': stamp.model_link,
#             'image_id': stamp.image_id,
#             'image_type': stamp.image_type,
#             'image_description': stamp.image_description,
#             'link300px': stamp.link300px,
#             'link1000px': stamp.link1000px
#         }
#         stamp_data.append(stamp_dict)
#     return jsonify(stamp_data)
