import Lake
open Lake DSL

package «tool_test01» where
  -- 您可以在這裡加入套件設定

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «ToolTest01»
