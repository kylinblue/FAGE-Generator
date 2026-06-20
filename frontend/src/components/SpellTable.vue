<template>
  <div class="spell-table">
    <el-table
      :data="spells"
      :height="height"
      :row-key="getRowKey"
      style="width: 100%"
    >
      <el-table-column
        prop="Name"
        label="Spell Name"
        min-width="180"
        sortable
        fixed
      />
      <el-table-column
        prop="Arcana"
        label="Arcana"
        width="150"
        sortable
      />
      <el-table-column
        prop="MP"
        label="MP Cost"
        width="90"
        sortable
      />
      <el-table-column
        prop="CastTime"
        label="Casting Time"
        width="130"
      />
      <el-table-column
        prop="TN"
        label="TN"
        width="70"
        sortable
      />
      <el-table-column
        prop="SpellType"
        label="Type"
        width="110"
        sortable
      />
      <el-table-column
        label="Action"
        width="180"
        fixed="right"
      >
        <template #default="scope">
          <el-button
            size="small"
            @click="handleViewDetails(scope.row)"
          >
            View Details
          </el-button>
          <el-button
            v-if="showRollButton"
            size="small"
            type="primary"
            @click="handleRoll(scope.row)"
          >
            Cast
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
const props = defineProps({
  spells: {
    type: Array,
    required: true,
    default: () => []
  },
  height: {
    type: String,
    default: '400px'
  },
  showRollButton: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['view-details', 'roll'])

// Generate unique row key
const getRowKey = (row) => {
  return row.Name || JSON.stringify(row)
}

// Handle view details button click
const handleViewDetails = (spell) => {
  emit('view-details', spell)
}

// Handle cast button click
const handleRoll = (spell) => {
  emit('roll', spell)
}
</script>

<style scoped>
.spell-table {
  width: 100%;
}
</style>
