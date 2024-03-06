import csv
from .management.commands._Logger import set_logger
from .management.commands.plot import SOLID, SOLUTION
from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = "base.html"


class ImageView(TemplateView):
    template_name = "solution/index.html"

    #変数としてグラフイメージをテンプレートに渡す
    def get_context_data(self, **kwargs):
        if "dimension" in self.request.GET:
            dimension = self.request.GET.get('dimension')

#        if "shape" in self.request.GET:
#            shape = self.request.GET.get('shape')
#
#        if "w" in self.request.GET:
#            width = self.request.GET.get('w')
#
#        if "h" in self.request.GET:
#            height = 'x' + self.request.GET.get('h')
#
#        if "d" in self.request.GET:
#            depth = 'x' + self.request.GET.get('d')
#
#        if "line" in self.request.GET:
#            line = self.request.GET.get('line')

#        file = dimension + '_' + shape + '_' + width + height + depth + ".txt"
#        solution = get_solution(file, line)

#        print(solution)
#        solution = SOLUTION('plane', 'square', '8', '8')
        solution = SOLUTION('solid', 'hollow', '3', '3', '9')
        solid = SOLID(3, 3, 9)

        image = solid.image(solution.get(5))
        context = super().get_context_data(**kwargs)
        context['image'] = image

        return context

    #get処理
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
