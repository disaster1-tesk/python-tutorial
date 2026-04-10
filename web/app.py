"""
Python 教程 Web 平台 - Flask 主应用
包含所有路由、业务逻辑和 API 端点
端口: 8502
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify, request, session, redirect, url_for

# 添加当前目录到路径
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from config import (
    MODULES, MODULE_CATEGORIES, APP_NAME, APP_ICON, APP_VERSION,
    get_module_info, get_category_modules, get_learning_path, get_module_dependencies, APP_PORT
)

# 绝对路径
MODULES_DIR = BASE_DIR.parent
DATA_DIR = BASE_DIR / 'data'
PROGRESS_FILE = DATA_DIR / 'progress.json'
ACHIEVEMENTS_FILE = DATA_DIR / 'achievements.json'
FAVORITES_FILE = DATA_DIR / 'favorites.json'

# Flask 应用
app = Flask(__name__)
app.secret_key = 'python-tutorial-secret-key-v2'
app.config['BASE_DIR'] = BASE_DIR
app.config['DATA_DIR'] = DATA_DIR
app.config['MODULES_DIR'] = MODULES_DIR


# ==================== 数据加载器 ====================

def load_json(filepath):
    """加载 JSON 文件"""
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_progress():
    """获取学习进度"""
    data = load_json(PROGRESS_FILE)
    if data is None:
        return {
            'modules': {},
            'exercises': [],
            'quizzes': [],
            'learning_days': [],
            'last_visit': None,
            'total_time': 0
        }
    return data


def save_progress(data):
    """保存学习进度"""
    save_json(PROGRESS_FILE, data)


def get_achievements():
    """获取成就数据"""
    data = load_json(ACHIEVEMENTS_FILE)
    if data is None:
        return {'achievements': [], 'unlocked': []}
    return data


def save_achievements(data):
    """保存成就数据"""
    save_json(ACHIEVEMENTS_FILE, data)


def get_favorites():
    """获取收藏数据"""
    data = load_json(FAVORITES_FILE)
    if data is None:
        return {'modules': [], 'exercises': [], 'quizzes': []}
    return data


def save_favorites(data):
    """保存收藏数据"""
    save_json(FAVORITES_FILE, data)


def update_module_status(module_id: str, status: str):
    """更新模块学习状态"""
    # 保存到JSON文件
    progress = get_progress()
    progress['modules'][module_id] = {
        'status': status,
        'updated_at': datetime.now().isoformat()
    }
    
    # 记录学习日期
    today = datetime.now().date().isoformat()
    if today not in progress.get('learning_days', []):
        progress.setdefault('learning_days', []).append(today)
    progress['last_visit'] = datetime.now().isoformat()
    
    save_progress(progress)
    
    # 检查成就
    check_achievements()


def mark_exercise_completed(exercise_id: str, correct: bool = False):
    """标记练习题完成"""
    # 保存到JSON文件
    progress = get_progress()
    existing = [i for i, e in enumerate(progress['exercises']) if str(e.get('id')) == str(exercise_id)]
    if not existing:
        progress['exercises'].append({
            'id': exercise_id,
            'completed_at': datetime.now().isoformat(),
            'correct': correct
        })
    else:
        # 更新为正确的
        if correct:
            progress['exercises'][existing[0]]['correct'] = True
            progress['exercises'][existing[0]]['completed_at'] = datetime.now().isoformat()
    save_progress(progress)
    check_achievements()


def mark_quiz_completed(quiz_id: str, score: int):
    """标记测验完成"""
    # 保存到JSON文件
    progress = get_progress()
    existing = [i for i, q in enumerate(progress['quizzes']) if str(q.get('id')) == str(quiz_id)]
    if not existing:
        progress['quizzes'].append({
            'id': quiz_id,
            'score': score,
            'completed_at': datetime.now().isoformat()
        })
    else:
        # 更新最高分
        if score > progress['quizzes'][existing[0]].get('score', 0):
            progress['quizzes'][existing[0]]['score'] = score
            progress['quizzes'][existing[0]]['completed_at'] = datetime.now().isoformat()
    save_progress(progress)
    check_achievements()


# ==================== 成就系统 ====================

ACHIEVEMENT_DEFINITIONS = [
    {"id": "first_step", "name": "初学者", "icon": "🏃", "description": "完成第一个模块", "condition": "modules_completed >= 1"},
    {"id": "ten_modules", "name": "勤奋学者", "icon": "📚", "description": "完成10个模块", "condition": "modules_completed >= 10"},
    {"id": "all_basics", "name": "基础达人", "icon": "🎓", "description": "完成所有基础阶段模块", "condition": "all_basics_completed"},
    {"id": "week_streak", "name": "连续学习", "icon": "🔥", "description": "7天连续学习", "condition": "streak >= 7"},
    {"id": "practice_master", "name": "练习大师", "icon": "💯", "description": "完成50道练习题", "condition": "exercises_completed >= 50"},
    {"id": "perfect_score", "name": "满分王者", "icon": "👑", "description": "测验获得满分", "condition": "perfect_quiz"},
    {"id": "explorer", "name": "探索者", "icon": "🧭", "description": "浏览所有模块", "condition": "all_modules_visited"},
]


def check_achievements():
    """检查并解锁成就"""
    progress = get_progress()
    achievements = get_achievements()
    unlocked_ids = achievements.get('unlocked', [])
    
    completed_count = sum(1 for m in progress['modules'].values() if m.get('status') == 'completed')
    exercises_count = len(progress.get('exercises', []))
    quizzes = progress.get('quizzes', [])
    
    # 检查连续学习
    learning_days = progress.get('learning_days', [])
    streak = 0
    if learning_days:
        dates = [datetime.fromisoformat(d).date() for d in learning_days]
        today = datetime.now().date()
        for i in range(len(dates) - 1, -1, -1):
            if (today - dates[i]).days <= i + 1:
                streak += 1
            else:
                break
    
    # 检查基础阶段完成
    basics_modules = [m['id'] for m in MODULES if m['category'] == '基础阶段']
    basics_completed = sum(1 for m in basics_modules if progress['modules'].get(m, {}).get('status') == 'completed')
    all_basics_done = basics_completed == len(basics_modules)
    
    # 检查满分测验
    perfect_quiz = any(q.get('score', 0) == 100 for q in quizzes)
    
    # 检查所有模块访问
    all_visited = len(progress['modules']) >= len(MODULES)
    
    for achievement in ACHIEVEMENT_DEFINITIONS:
        if achievement['id'] in unlocked_ids:
            continue
        
        # 评估条件
        cond = achievement['condition']
        should_unlock = False
        
        if 'modules_completed' in cond:
            threshold = int(cond.split('>=')[1])
            should_unlock = completed_count >= threshold
        elif 'exercises_completed' in cond:
            threshold = int(cond.split('>=')[1])
            should_unlock = exercises_count >= threshold
        elif 'all_basics_completed' in cond:
            should_unlock = all_basics_done
        elif 'streak' in cond:
            threshold = int(cond.split('>=')[1])
            should_unlock = streak >= threshold
        elif 'perfect_quiz' in cond:
            should_unlock = perfect_quiz
        elif 'all_modules_visited' in cond:
            should_unlock = all_visited
        
        if should_unlock:
            unlocked_ids.append(achievement['id'])
            achievements['achievements'].append({
                'id': achievement['id'],
                'unlocked_at': datetime.now().isoformat()
            })
    
    achievements['unlocked'] = unlocked_ids
    save_achievements(achievements)


# ==================== 内容加载 ====================

def get_module_description(module_id: str) -> str:
    """获取模块知识点内容"""
    md_file = MODULES_DIR / module_id / 'description.md'
    if md_file.exists():
        with open(md_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def get_module_example(module_id: str) -> str:
    """获取模块示例代码"""
    py_file = MODULES_DIR / module_id / 'example.py'
    if py_file.exists():
        with open(py_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def get_categories():
    """获取所有分类"""
    return MODULE_CATEGORIES


def get_all_exercises() -> list:
    """获取所有练习题"""
    exercises_file = DATA_DIR / 'exercises.json'
    if exercises_file.exists():
        return load_json(exercises_file)
    return []


def get_exercises(module_id: str = None) -> list:
    """获取指定模块的练习题"""
    all_ex = get_all_exercises()
    if module_id:
        return [e for e in all_ex if e.get('module') == module_id]
    return all_ex


def get_all_quizzes() -> list:
    """获取所有测验题"""
    quizzes_file = DATA_DIR / 'quizzes.json'
    if quizzes_file.exists():
        return load_json(quizzes_file)
    return []


def get_quizzes(module_id: str = None) -> list:
    """获取指定模块的测验题"""
    all_q = get_all_quizzes()
    if module_id:
        return [q for q in all_q if q.get('module_id') == module_id]
    return all_q


def search_content(keyword: str) -> dict:
    """全局搜索"""
    results = {
        'modules': [],
        'exercises': [],
        'quizzes': []
    }
    
    if not keyword:
        return results
    
    keyword = keyword.lower()
    
    # 搜索模块
    for module in MODULES:
        if keyword in module['name'].lower():
            results['modules'].append(module)
    
    # 搜索练习题
    for ex in get_all_exercises():
        if keyword in ex.get('title', '').lower() or keyword in ex.get('description', '').lower():
            results['exercises'].append(ex)
    
    # 搜索测验题
    for q in get_all_quizzes():
        if keyword in q.get('question', '').lower():
            results['quizzes'].append(q)
    
    return results


# 练习题文件路径
EXERCISES_FILE = DATA_DIR / 'exercises.json'


def save_exercises(exercises_list: list):
    """保存练习题列表到 JSON 文件"""
    # 备份原文件
    if EXERCISES_FILE.exists():
        import shutil
        backup_file = DATA_DIR / 'exercises.json.bak'
        shutil.copy2(EXERCISES_FILE, backup_file)
    save_json(EXERCISES_FILE, exercises_list)


def generate_exercise_id(module_id: str) -> str:
    """生成唯一的练习题 ID"""
    import time
    timestamp = int(time.time() * 1000)
    return f'ex_user_{module_id}_{timestamp}'


def save_module_description(module_id: str, content: str):
    """保存模块知识点内容到 Markdown 文件"""
    md_file = MODULES_DIR / module_id / 'description.md'
    # 确保目录存在
    md_file.parent.mkdir(parents=True, exist_ok=True)
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)


# ==================== 路由 ====================

@app.route('/')
def index():
    """首页"""
    progress = get_progress()
    achievements = get_achievements()
    
    total = len(MODULES)
    completed = sum(1 for m in progress['modules'].values() if m.get('status') == 'completed')
    in_progress = sum(1 for m in progress['modules'].values() if m.get('status') == 'in_progress')
    unlocked_count = len(achievements.get('unlocked', []))
    
    # 按分类组织模块
    categories = get_categories()
    modules_by_category = {}
    for cat in categories:
        modules_by_category[cat] = get_category_modules(cat)
    
    # 获取学习路径
    learning_path = get_learning_path()
    
    # 今日成就检查
    today = datetime.now().date().isoformat()
    learning_days = progress.get('learning_days', [])
    streak = 0
    if learning_days:
        dates = [datetime.fromisoformat(d).date() for d in learning_days]
        today_date = datetime.now().date()
        streak = sum(1 for d in dates if (today_date - d).days < 7)
    
    return render_template('index.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         APP_VERSION=APP_VERSION,
                         modules=MODULES,
                         categories=categories,
                         modules_by_category=modules_by_category,
                         progress=progress,
                         achievements=achievements,
                         total=total,
                         completed=completed,
                         in_progress=in_progress,
                         unlocked_count=unlocked_count,
                         learning_path=learning_path,
                         streak=streak)


@app.route('/learn/<module_id>')
def learn(module_id):
    """知识学习页面"""
    module_info = get_module_info(module_id)
    if not module_info:
        return "模块不存在", 404
    
    description = get_module_description(module_id)
    example = get_module_example(module_id)
    
    # 获取依赖
    dependencies = get_module_dependencies(module_id)
    dependency_modules = [get_module_info(d) for d in dependencies]
    
    # 进度状态
    progress = get_progress()
    module_status = progress['modules'].get(module_id, {}).get('status', 'not_started')
    
    # 收藏状态
    favorites = get_favorites()
    is_favorited = module_id in favorites.get('modules', [])
    
    all_modules = MODULES
    categories = get_categories()
    
    # 更新学习状态（标记为进行中）
    if module_status == 'not_started':
        update_module_status(module_id, 'in_progress')
        module_status = 'in_progress'
    
    return render_template('learn.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         module_info=module_info,
                         description=description,
                         example=example,
                         dependencies=dependency_modules,
                         module_status=module_status,
                         is_favorited=is_favorited,
                         modules=all_modules,
                         categories=categories,
                         progress=progress)


@app.route('/exercises')
@app.route('/exercises/<module_id>')
def exercises(module_id=None):
    """练习题页面 - 一次只显示一道题"""
    progress = get_progress()
    favorites = get_favorites()
    categories = get_categories()
    
    # 获取筛选参数
    difficulty = request.args.get('difficulty', 'all')
    index = request.args.get('index', 0, type=int)
    exercise_id = request.args.get('exercise_id')  # 从搜索跳转时使用
    
    if module_id:
        module_info = get_module_info(module_id)
        exercises_list = get_exercises(module_id)
    else:
        module_info = None
        exercises_list = get_all_exercises()
    
    # 按难度筛选
    if difficulty and difficulty != 'all':
        exercises_list = [ex for ex in exercises_list if ex.get('difficulty') == difficulty]
    
    # 添加收藏状态
    favorited_ids = favorites.get('exercises', [])
    for ex in exercises_list:
        ex['is_favorited'] = ex.get('id') in favorited_ids
    
    # 计算当前题目
    total_count = len(exercises_list)
    
    # 如果是从搜索跳转过来的，根据 exercise_id 找到对应的题目索引
    if exercise_id:
        for i, ex in enumerate(exercises_list):
            if ex.get('id') == exercise_id:
                index = i
                break
    
    current_index = min(index, max(0, total_count - 1)) if total_count > 0 else 0
    current_exercise = exercises_list[current_index] if exercises_list else None
    
    return render_template('exercises.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         modules=MODULES,
                         categories=categories,
                         current_module=module_id,
                         module_info=module_info,
                         exercises=exercises_list,
                         exercise=current_exercise,
                         current_index=current_index,
                         total_count=total_count,
                         current_difficulty=difficulty,
                         progress=progress,
                         favorites=favorites)


@app.route('/quiz')
@app.route('/quiz/<module_id>')
def quiz(module_id=None):
    """测验页面 - 一次只显示一道题"""
    progress = get_progress()
    favorites = get_favorites()
    categories = get_categories()
    
    # 获取当前索引
    index = request.args.get('index', 0, type=int)
    
    # 支持path参数和query参数两种方式
    if not module_id:
        module_id = request.args.get('module_id')
    
    if module_id:
        module_info = get_module_info(module_id)
        quizzes_list = get_quizzes(module_id)
    else:
        module_info = None
        quizzes_list = get_all_quizzes()
    
    # 计算当前题目
    total_count = len(quizzes_list)
    current_index = min(index, max(0, total_count - 1)) if total_count > 0 else 0
    current_quiz = quizzes_list[current_index] if quizzes_list else None
    
    return render_template('quiz.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         modules=MODULES,
                         categories=categories,
                         current_module=module_id,
                         module_info=module_info,
                         quizzes=quizzes_list,
                         quiz=current_quiz,
                         current_index=current_index,
                         total_count=total_count,
                         progress=progress,
                         favorites=favorites)



@app.route('/stats')
def stats():
    """学习统计页面"""
    progress = get_progress()
    achievements = get_achievements()
    exercises_list = get_all_exercises()
    quizzes_list = get_all_quizzes()
    categories = get_categories()
    
    # 计算统计数据
    completed_count = sum(1 for m in progress['modules'].values() if m.get('status') == 'completed')
    exercises_count = len(progress.get('exercises', []))
    quizzes_count = len(progress.get('quizzes', []))
    
    # 正确率
    correct_count = sum(1 for e in progress.get('exercises', []) if e.get('correct', False))
    correct_rate = (correct_count / exercises_count * 100) if exercises_count > 0 else 0
    
    return render_template('stats.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         modules=MODULES,
                         categories=categories,
                         progress=progress,
                         achievements=achievements,
                         exercises=exercises_list,
                         quizzes=quizzes_list,
                         completed_count=completed_count,
                         exercises_count=exercises_count,
                         quizzes_count=quizzes_count,
                         correct_rate=correct_rate)


@app.route('/achievements')
def achievements():
    """成就页面"""
    achievements_data = get_achievements()
    progress = get_progress()
    
    unlocked_ids = achievements_data.get('unlocked', [])
    
    # 构建成就列表
    achievement_list = []
    for ach in ACHIEVEMENT_DEFINITIONS:
        is_unlocked = ach['id'] in unlocked_ids
        unlock_info = None
        
        if is_unlocked:
            for a in achievements_data.get('achievements', []):
                if a['id'] == ach['id']:
                    unlock_info = a
                    break
        
        achievement_list.append({
            **ach,
            'unlocked': is_unlocked,
            'unlocked_at': unlock_info.get('unlocked_at') if unlock_info else None
        })
    
    return render_template('achievements.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         achievements=achievement_list,
                         progress=progress)


@app.route('/favorites')
def favorites_page():
    """收藏页面"""
    favorites = get_favorites()
    progress = get_progress()
    
    # 获取收藏的模块
    favorited_modules = [get_module_info(mid) for mid in favorites.get('modules', [])]
    
    # 获取收藏的练习题
    favorited_exercises = [ex for ex in get_all_exercises() if ex.get('id') in favorites.get('exercises', [])]
    
    # 获取收藏的测验
    favorited_quizzes = [q for q in get_all_quizzes() if q.get('id') in favorites.get('quizzes', [])]
    
    return render_template('favorites.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         modules=MODULES,
                         favorited_modules=favorited_modules,
                         favorited_exercises=favorited_exercises,
                         favorited_quizzes=favorited_quizzes,
                         progress=progress)


# ==================== API 路由 ====================

@app.route('/api/progress', methods=['GET'])
def api_progress():
    """获取进度 API"""
    return jsonify(get_progress())


@app.route('/api/progress/module/<module_id>', methods=['POST'])
def api_update_module(module_id):
    """更新模块状态"""
    data = request.get_json()
    status = data.get('status', 'in_progress')
    update_module_status(module_id, status)
    return jsonify({'success': True})


@app.route('/api/exercises', methods=['GET'])
def api_exercises():
    """获取练习题 API"""
    module_id = request.args.get('module')
    return jsonify(get_exercises(module_id))


@app.route('/api/exercises/<exercise_id>/complete', methods=['POST'])
def api_exercise_complete(exercise_id):
    """标记练习题完成"""
    data = request.get_json()
    correct = data.get('correct', False)
    mark_exercise_completed(exercise_id, correct)
    return jsonify({'success': True})


@app.route('/api/quizzes', methods=['GET'])
def api_quizzes():
    """获取测验题 API"""
    module_id = request.args.get('module')
    return jsonify(get_quizzes(module_id))


@app.route('/api/quizzes/<quiz_id>/complete', methods=['POST'])
def api_quiz_complete(quiz_id):
    """提交测验"""
    data = request.get_json()
    score = data.get('score', 0)
    user_answer = data.get('answer', '')
    mark_quiz_completed(quiz_id, score)
    return jsonify({'success': True})


@app.route('/api/modules', methods=['GET'])
def api_modules():
    """获取所有模块 API"""
    return jsonify(MODULES)


@app.route('/api/search', methods=['GET'])
def api_search():
    """搜索 API"""
    keyword = request.args.get('q', '')
    return jsonify(search_content(keyword))


@app.route('/api/favorites', methods=['GET', 'POST'])
def api_favorites():
    """收藏 API"""
    if request.method == 'POST':
        data = request.get_json()
        fav_type = data.get('type')  # 'modules', 'exercises', 'quizzes'
        item_id = data.get('id')
        
        favorites = get_favorites()
        if item_id not in favorites.get(fav_type, []):
            favorites.setdefault(fav_type, []).append(item_id)
            save_favorites(favorites)
        
        return jsonify({'success': True})
    else:
        return jsonify(get_favorites())


@app.route('/api/favorites/<fav_type>/<item_id>', methods=['DELETE'])
def api_remove_favorite(fav_type, item_id):
    """取消收藏"""
    favorites = get_favorites()
    if item_id in favorites.get(fav_type, []):
        favorites[fav_type].remove(item_id)
        save_favorites(favorites)
    return jsonify({'success': True})


@app.route('/api/achievements', methods=['GET'])
def api_achievements():
    """成就 API"""
    return jsonify(get_achievements())


# ==================== 内容管理 API ====================

@app.route('/api/exercises', methods=['GET'])
def api_get_exercises():
    """获取所有练习题（支持按模块筛选）"""
    module_filter = request.args.get('module', '')
    exercises_list = get_all_exercises()
    
    if module_filter:
        exercises_list = [e for e in exercises_list if e.get('module') == module_filter]
    
    return jsonify(exercises_list)


@app.route('/api/exercises', methods=['POST'])
def api_create_exercise():
    """创建新练习题"""
    data = request.get_json()
    
    # 必填字段校验
    required = ['title', 'module', 'difficulty', 'description']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400
    
    # 难度枚举校验
    if data.get('difficulty') not in ['easy', 'medium', 'hard']:
        return jsonify({'success': False, 'error': '难度必须是 easy/medium/hard'}), 400
    
    # 生成 ID
    exercise_id = generate_exercise_id(data['module'])
    
    new_exercise = {
        'id': exercise_id,
        'module': data.get('module', ''),
        'title': data.get('title', ''),
        'difficulty': data.get('difficulty', 'easy'),
        'points': int(data.get('points', 10)),
        'description': data.get('description', ''),
        'starter_code': data.get('starter_code', ''),
        'solution': data.get('solution', ''),
        'tags': [t.strip() for t in data.get('tags', '').split(',') if t.strip()] if isinstance(data.get('tags'), str) else (data.get('tags') or [])
    }
    
    exercises_list = get_all_exercises()
    exercises_list.append(new_exercise)
    save_exercises(exercises_list)
    
    return jsonify({'success': True, 'exercise': new_exercise})


@app.route('/api/exercises/<exercise_id>', methods=['PUT'])
def api_update_exercise(exercise_id):
    """更新练习题"""
    data = request.get_json()
    exercises_list = get_all_exercises()
    
    # 查找目标题目
    target_idx = None
    for i, ex in enumerate(exercises_list):
        if str(ex.get('id')) == str(exercise_id):
            target_idx = i
            break
    
    if target_idx is None:
        return jsonify({'success': False, 'error': '题目不存在'}), 404
    
    # 更新字段（保留未提供的字段）
    ex = exercises_list[target_idx]
    ex['title'] = data.get('title', ex.get('title', ''))
    ex['module'] = data.get('module', ex.get('module', ''))
    ex['difficulty'] = data.get('difficulty', ex.get('difficulty', 'easy'))
    ex['points'] = int(data.get('points', ex.get('points', 10)))
    ex['description'] = data.get('description', ex.get('description', ''))
    ex['starter_code'] = data.get('starter_code', ex.get('starter_code', ''))
    ex['solution'] = data.get('solution', ex.get('solution', ''))
    
    tags_data = data.get('tags')
    if isinstance(tags_data, str):
        ex['tags'] = [t.strip() for t in tags_data.split(',') if t.strip()]
    elif isinstance(tags_data, list):
        ex['tags'] = tags_data
    
    save_exercises(exercises_list)
    return jsonify({'success': True, 'exercise': ex})


@app.route('/api/exercises/<exercise_id>', methods=['DELETE'])
def api_delete_exercise(exercise_id):
    """删除练习题"""
    exercises_list = get_all_exercises()
    original_len = len(exercises_list)
    exercises_list = [ex for ex in exercises_list if str(ex.get('id')) != str(exercise_id)]
    
    if len(exercises_list) == original_len:
        return jsonify({'success': False, 'error': '题目不存在'}), 404
    
    save_exercises(exercises_list)
    return jsonify({'success': True})


@app.route('/api/modules/<module_id>/content', methods=['GET'])
def api_get_module_content(module_id):
    """获取模块知识点内容"""
    module_info = get_module_info(module_id)
    if not module_info:
        return jsonify({'success': False, 'error': '模块不存在'}), 404
    
    content = get_module_description(module_id)
    return jsonify({
        'success': True,
        'module_id': module_id,
        'content': content,
        'module_info': module_info
    })


@app.route('/api/modules/<module_id>/content', methods=['PUT'])
def api_save_module_content(module_id):
    """保存模块知识点内容"""
    module_info = get_module_info(module_id)
    if not module_info:
        return jsonify({'success': False, 'error': '模块不存在'}), 404
    
    data = request.get_json()
    content = data.get('content', '')
    
    if not content:
        return jsonify({'success': False, 'error': '内容不能为空'}), 400
    
    try:
        save_module_description(module_id, content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': f'保存失败: {str(e)}'}), 500


# ==================== 管理页面路由 ====================

@app.route('/admin')
def admin():
    """内容管理页面"""
    categories = get_categories()
    exercises_list = get_all_exercises()
    
    return render_template('admin.html',
                         APP_NAME=APP_NAME,
                         APP_ICON=APP_ICON,
                         modules=MODULES,
                         categories=categories,
                         exercises=exercises_list)


# ==================== AI 助手 ====================

@app.route('/api/ai/chat', methods=['POST'])
def api_ai_chat():
    """AI 对话 API"""
    data = request.get_json()
    messages = data.get('messages', [])
    provider = data.get('provider', 'ollama')
    api_config = data.get('config', {})
    
    # 这里需要实现具体的 AI 调用逻辑
    # 可以支持 Ollama, OpenAI, Claude 等
    import requests
    
    try:
        if provider == 'ollama':
            api_url = api_config.get('api_url', 'http://localhost:11434')
            model = api_config.get('model', 'llama3')
            
            response = requests.post(
                f'{api_url}/api/chat',
                json={
                    'model': model,
                    'messages': messages,
                    'stream': False
                },
                timeout=60
            )
            result = response.json()
            return jsonify({
                'success': True,
                'message': {'role': 'assistant', 'content': result.get('message', {}).get('content', '')}
            })
        
        elif provider == 'openai':
            api_key = api_config.get('api_key', '')
            model = api_config.get('model', 'gpt-3.5-turbo')
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': model,
                    'messages': messages
                },
                timeout=60
            )
            result = response.json()
            return jsonify({
                'success': True,
                'message': {'role': 'assistant', 'content': result['choices'][0]['message']['content']}
            })
        
        elif provider == 'claude':
            api_key = api_config.get('api_key', '')
            model = api_config.get('model', 'claude-3-haiku-20240307')
            
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': model,
                    'max_tokens': 1024,
                    'messages': messages
                },
                timeout=60
            )
            result = response.json()
            return jsonify({
                'success': True,
                'message': {'role': 'assistant', 'content': result['content'][0]['text']}
            })
        
        else:
            return jsonify({'success': False, 'error': 'Unknown provider'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# ==================== 启动 ====================

if __name__ == '__main__':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 50)
    print(f"{APP_ICON} {APP_NAME}")
    print(f"版本: {APP_VERSION}")
    print("=" * 50)
    print(f"访问地址: http://localhost:{APP_PORT}")
    print("按 Ctrl+C 停止服务")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=APP_PORT, debug=True)
