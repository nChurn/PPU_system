from app_models.models import PPU, Effect, Category, Acc


def create_ppu(request, info):
        print(dir(request))
        
        print('\n' * 100)
        title = request.data['title']
        problem = request.data['problem']
        solution = request.data['solution']
        author = Acc.objects.get(username=info.get('username'))
        category = Category.objects.get(title=request.data['category'])
        effect = Effect.objects.get(title=request.data['effect'])
        


        ppu = PPU(
            title = title,
            problem = problem,
            solution = solution,
            author = author,
            category = category,
            effect = effect
        )

        if request.data['co_author'] and request.data['co_author_procent']:
            ppu.co_author = Acc.objects.get(username=request.data['co_author'])
            ppu.co_author_procent = request.data['co_author_procent']
        
        try:
            ppu.save()
            return ppu
        except Exception as e:
            return e

"""
def create_vned_ppu(ppu, data):
    vned_ppu = VnedPPU()
    try:
        vned_ppu.author = ppu.author
    except:
        pass
    
    try:
        vned_ppu.title = ppu.title
    except:
        pass
    
    try:
        vned_ppu.problem = ppu.problem
    except:
        pass
    
    try:
        vned_ppu.solution = ppu.solution
    except:
        pass
    
    try:
        vned_ppu.file = ppu.file
    except:
        pass
    
    try:
        vned_ppu.co_author = ppu.co_author
    except:
        pass
    
    try:
        vned_ppu.co_author_procent = ppu.co_author_procent
    except:
        pass
    
    try:
        vned_ppu.category = ppu.category
    except:
        pass
    
    try:
        vned_ppu.effect = ppu.effect
    except:
        pass
    
    try:
        vned_ppu.effect = ppu.effect
    except:
        pass
    
    try:
        vned_ppu.moder = ppu.moder
    except:
        pass

    #ppu.delete()
#    vned_ppu.save()
    return vned_ppu
    
#def update_ppu(request, info)
"""