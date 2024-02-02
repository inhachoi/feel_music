# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for
import datetime
app = Flask(__name__)
# DB 기본 코드

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)
    video_url = db.Column(db.String(100), nullable=False)
    music_content = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer, nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    review_content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(200), nullable=False)


class Feel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feeling = db.Column(db.String(100), nullable=False)
    feeling_detail = db.Column(db.String(100), nullable=False)
    feeling_detail_cnt = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template('intro.html')


# 첫번쨰 감정
emotions = ['슬픔', '행복', '분노']
#
feelings = {
    "슬픔": ["우울", "미련", "좌절"],
    "행복": ["설레임", "즐거움", "성취감"],
    "분노": ["배신감", "불쾌감", "원망"]
}


@app.route("/survey1/")
def survey1():
    return render_template('survey1.html')


@app.route("/survey2/<emotion>")
def survey2(emotion):
    if (emotion == "슬픔"):
        emotion_list = feelings.get(emotion, [])
    elif (emotion == "행복"):
        emotion_list = feelings.get(emotion, [])
    else:
        emotion_list = feelings.get(emotion, [])
    return render_template('survey2.html', emotion_list=emotion_list, emotion=emotion)


@app.route("/survey3/<emotion>/<emotion_list>")
def survey3(emotion, emotion_list):
    feel_list = Feel.query.all()
    return render_template('survey3.html', emotion=emotion, emotion_list=emotion_list, feel_list=feel_list)


def get_comment_count(song_id):
    return Review.query.filter_by(song_id=song_id).count()


@app.route("/music")
def music():
    feeling = request.args.get('emotion_list')
    emotion = request.args.get('emotion')

    song_list = Song.query.filter_by(category=feeling).all()
    # 아직 수정 중
    song_id = request.args.get('song_id')

    return render_template('music.html', data=song_list, get_comment_count=get_comment_count, emotion=emotion, feeling=feeling)


@app.route("/music/detail")
def music_detail():
    song_id = request.args.get('song_id')
    # Song 테이블에서 title,artist,앨범 커버, 음원 가져오기
    song_info = Song.query.filter_by(id=song_id).all()

    # 저장된 리뷰들 가져오기F
    reviews = Review.query.filter_by(song_id=song_id).all()

    return render_template('music_detail.html', song=song_info, review=reviews)

# 음악 좋아요 증가 함수


@app.route("/like/", methods=['POST'])
def like():
    # 좋아요 수 증가
    song_id = request.args.get('song_id')
    song = Song.query.get(song_id)
    song.count += 1
    db.session.commit()

    # 리다이렉션
    return redirect(url_for('music_detail', song_id=song_id))

# post 메소드로 리뷰 작성


@app.route("/music/detail/create/", methods=['POST'])
def review_create():
    song_id = request.args.get('song_id')
    # song = Song.query.get(song_id)

    # 폼에서 전달된 리뷰 내용 저장
    if request.method == 'POST':
        review_content = request.form.get('review_content')
        if review_content:
            new_review = Review(
                song_id=song_id, review_content=review_content, date=datetime.datetime.now().strftime('%Y-%m-%d'))
            db.session.add(new_review)
            db.session.commit()

    # 리뷰 작성 후 리뷰 페이지로 리다이렉션
    return redirect(url_for('music_detail', song_id=song_id))


if __name__ == "__main__":
    app.run(debug=True)
