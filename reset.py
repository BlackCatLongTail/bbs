from models import reset_database
from models.user import User
from models.topic import Topic
from models.reply import Reply
from models.board import Board
from models.mail import Mail
from models.user_role import UserRole


def main():
    reset_database()

    User.new(
        username='wendy',
        password='123',
        role=UserRole.admin,
        avatar='/user/avatar/4.jpg'
    )

    Board.new(
        title='good',
    )

    Board.new(
        title='share',
    )


if __name__ == '__main__':
    main()
