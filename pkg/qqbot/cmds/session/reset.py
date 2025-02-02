from ..mgr import AbstractCommandNode, Context

import pkg.openai.session
import pkg.utils.context


@AbstractCommandNode.register(
    parent=None,
    name='reset',
    description='重置当前会话',
    usage='!reset',
    aliases=[],
    privilege=1
)
class ResetCommand(AbstractCommandNode):
    @classmethod
    def process(cls, ctx: Context) -> tuple[bool, list]:
        params = ctx.params
        session_name = ctx.session_name
        
        reply = ""

        if len(params) == 0:
            pkg.openai.session.get_session(session_name).reset(explicit=True)
            reply = ["[bot]会话已重置"]
        else:
            try:
                import pkg.openai.dprompt as dprompt
                pkg.openai.session.get_session(session_name).reset(explicit=True, use_prompt=params[0])
                reply = ["[bot]会话已重置，使用场景预设:{}".format(dprompt.mode_inst().get_full_name(params[0]))]
            except Exception as e:
                reply = ["[bot]会话重置失败：{}".format(e)]
        
        return True, reply