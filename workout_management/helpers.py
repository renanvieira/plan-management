from flask import current_app as app


class PaginatorHelper:

    @staticmethod
    def get_paginator_dict(paginator):
        paginator_schema = dict()
        paginator_schema["total"] = paginator.total
        paginator_schema["total_pages"] = paginator.pages
        paginator_schema["has_more"] = paginator.has_next
        paginator_schema["items"] = paginator.items

        return paginator_schema


class MailTextHelper:

    @staticmethod
    def get_plan_changed_template(plan):
        with app.open_resource("static/plan_changed_template.txt") as f:
            mail_template = f.read().decode("utf-8")
            with app.open_resource("static/exercise_template.txt") as file_exercise:
                exercise_tempalte = file_exercise.read().decode("utf-8")

                exercise_content = ''
                for day in plan.days:
                    exercise_content += "<h3>Day {}</h3>".format(day.number)
                    for exercise in day.exercises:
                        exercise_content += exercise_tempalte.format(exercise.name, exercise.sets, exercise.reps)

            return mail_template.format(plan.name, exercise_content)

    @staticmethod
    def get_associated_template(user, plan):
        with app.open_resource("static/user_associated_template.txt") as f:
            mail_template = f.read().decode("utf-8")
            return mail_template.format(user.full_name, plan.name)
